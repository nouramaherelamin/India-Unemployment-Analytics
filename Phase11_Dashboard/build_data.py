import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
COVID_START = pd.Timestamp("2020-03-01")

BASE = Path(__file__).resolve().parent
DATA_IN = BASE / "data" / "Unemployment_in_India.csv"
OUT = BASE / "data"
OUT.mkdir(parents=True, exist_ok=True)

UNEMP = "Estimated Unemployment Rate (%)"
PART = "Estimated Labour Participation Rate (%)"
EMPLOYED = "Estimated Employed"

# ------------------------------------------------------------
# 1. Load + clean (mirrors notebook Section 5)
# ------------------------------------------------------------
df = pd.read_csv(DATA_IN)
df.columns = df.columns.str.strip()
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

df = df.loc[~df.isna().all(axis=1)].copy()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)

for col in [UNEMP, EMPLOYED, PART]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Region"] = df["Region"].astype(str).str.strip()
df["Area"] = df["Area"].astype(str).str.strip()
df["Period"] = np.where(df["Date"] < COVID_START, "Pre-COVID", "COVID")

clean_df = df.copy()
clean_df.to_csv(OUT / "cleaned_data.csv", index=False)
print("cleaned_data.csv:", clean_df.shape)

# ------------------------------------------------------------
# 2. Coverage audit
# ------------------------------------------------------------
expected_months = pd.date_range(clean_df["Date"].min(), clean_df["Date"].max(), freq="ME")

# Coverage is assessed per Region-Area combination: a region only counts as
# "fully covered" if BOTH its Rural and Urban series have all 14 months.
coverage_table = clean_df.groupby(["Region", "Area"])["Date"].nunique().reset_index(name="months_observed")
coverage_table["complete"] = coverage_table["months_observed"] == len(expected_months)
region_fully_complete = coverage_table.groupby("Region")["complete"].all()

fully_covered_regions = sorted(region_fully_complete[region_fully_complete].index.tolist())
incomplete_regions = sorted(region_fully_complete[~region_fully_complete].index.tolist())
print("Fully covered:", len(fully_covered_regions), "Incomplete:", len(incomplete_regions))

# ------------------------------------------------------------
# 3. Regional profile
# ------------------------------------------------------------
regional_profile = clean_df.groupby("Region")[UNEMP].agg(
    Overall_Mean="mean", Overall_Median="median", Overall_SD="std"
)

pre_regional = clean_df[clean_df["Period"] == "Pre-COVID"].groupby("Region")[UNEMP].mean().rename("Pre_COVID_Mean")
covid_regional = clean_df[clean_df["Period"] == "COVID"].groupby("Region")[UNEMP].mean().rename("COVID_Mean")

regional_profile = pd.concat([regional_profile, pre_regional, covid_regional], axis=1)
regional_profile["Shock_Magnitude_pp"] = regional_profile["COVID_Mean"] - regional_profile["Pre_COVID_Mean"]
regional_profile["Shock_%_of_Baseline"] = regional_profile["Shock_Magnitude_pp"] / regional_profile["Pre_COVID_Mean"] * 100
regional_profile["CV_%"] = regional_profile["Overall_SD"] / regional_profile["Overall_Mean"] * 100

trend_records = []
for region, group in clean_df.groupby("Region"):
    group = group.sort_values("Date").copy()
    x = np.arange(len(group))
    if len(group) >= 3:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, group[UNEMP])
    else:
        slope = r_value = p_value = np.nan
    june = group.loc[group["Date"] == pd.Timestamp("2020-06-30"), UNEMP]
    trend_records.append({
        "Region": region,
        "Trend_Slope_pp_per_Month": slope,
        "Trend_p_value": p_value,
        "Trend_R2": r_value ** 2 if pd.notna(r_value) else np.nan,
        "June_2020_Mean": june.mean() if len(june) else np.nan,
    })
regional_trends = pd.DataFrame(trend_records).set_index("Region")
regional_profile = regional_profile.join(regional_trends)
regional_profile["June_vs_Pre_COVID_Gap"] = regional_profile["June_2020_Mean"] - regional_profile["Pre_COVID_Mean"]

regional_profile = regional_profile.reset_index().rename(columns={"index": "Region"})
regional_profile["Coverage_Status"] = np.where(
    regional_profile["Region"].isin(fully_covered_regions), "Fully covered", "Incomplete"
)
regional_profile["Recovery_Status"] = np.where(
    regional_profile["June_vs_Pre_COVID_Gap"] <= 0.5, "Recovering toward baseline", "Still elevated vs baseline"
)
regional_profile.to_csv(OUT / "regional_profiles.csv", index=False)
print("regional_profiles.csv:", regional_profile.shape)

# ------------------------------------------------------------
# 4. Correlation tests
# ------------------------------------------------------------
def correlation_test(x, y):
    pearson_r, pearson_p = stats.pearsonr(x, y)
    spearman_rho, spearman_p = stats.spearmanr(x, y)
    return {"Pearson_r": pearson_r, "Pearson_p": pearson_p, "Spearman_rho": spearman_rho, "Spearman_p": spearman_p}

corr_records = []
for period in ["All", "Pre-COVID", "COVID"]:
    subset = clean_df if period == "All" else clean_df[clean_df["Period"] == period]
    for target in [PART, EMPLOYED]:
        result = correlation_test(subset[UNEMP], subset[target])
        corr_records.append({"Period": period, "Relationship": f"Unemployment vs {target}", **result})

correlation_tests = pd.DataFrame(corr_records)
correlation_tests.to_csv(OUT / "correlation_tests.csv", index=False)
print("correlation_tests.csv:", correlation_tests.shape)

# ------------------------------------------------------------
# 5. Mann-Whitney (balanced Rural vs Urban) + Kruskal-Wallis (regional)
# ------------------------------------------------------------
balanced_region_df = clean_df[clean_df["Region"].isin(fully_covered_regions)].copy()

def rank_biserial_from_u(u, n1, n2):
    return 1 - (2 * u) / (n1 * n2)

mw_records = []
for period in ["Pre-COVID", "COVID"]:
    subset = balanced_region_df[balanced_region_df["Period"] == period]
    rural = subset.loc[subset["Area"].str.lower() == "rural", UNEMP].dropna()
    urban = subset.loc[subset["Area"].str.lower() == "urban", UNEMP].dropna()
    u_stat, p_value = stats.mannwhitneyu(rural, urban, alternative="two-sided")
    mw_records.append({
        "Period": period, "Rural_N": len(rural), "Urban_N": len(urban),
        "Rural_Median": rural.median(), "Urban_Median": urban.median(),
        "U": u_stat, "p_value": p_value,
        "Rank_Biserial": rank_biserial_from_u(u_stat, len(rural), len(urban)),
    })
mann_whitney_results = pd.DataFrame(mw_records)
mann_whitney_results.to_csv(OUT / "mann_whitney_balanced_rural_vs_urban.csv", index=False)
print("mann_whitney:", mann_whitney_results.shape)

kw_records = []
for period in ["Pre-COVID", "COVID"]:
    subset = balanced_region_df[balanced_region_df["Period"] == period]
    groups = [g[UNEMP].dropna().values for _, g in subset.groupby("Region")]
    h_stat, p_value = stats.kruskal(*groups)
    n = sum(len(g) for g in groups)
    k = len(groups)
    epsilon_sq = (h_stat - k + 1) / (n - k)
    kw_records.append({"Period": period, "H": h_stat, "p_value": p_value, "epsilon_squared": epsilon_sq, "regions": k, "observations": n})
kruskal_results = pd.DataFrame(kw_records)
kruskal_results.to_csv(OUT / "kruskal_wallis_regional.csv", index=False)
print("kruskal:", kruskal_results.shape)

# ------------------------------------------------------------
# 6. Clustering (K-Means + PCA)
# ------------------------------------------------------------
participation_profile = (
    clean_df.groupby(["Region", "Period"])[PART]
    .mean()
    .unstack()
    .rename(columns={"Pre-COVID": "Pre_COVID_Mean_Participation", "COVID": "COVID_Mean_Participation"})
)

rp_indexed = regional_profile.set_index("Region")
cluster_features = rp_indexed.join(participation_profile)

feature_cols = [
    "Pre_COVID_Mean", "COVID_Mean", "Shock_Magnitude_pp", "CV_%",
    "Trend_Slope_pp_per_Month", "Pre_COVID_Mean_Participation", "COVID_Mean_Participation",
]
cluster_features = cluster_features[feature_cols].dropna()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(cluster_features)

pca = PCA()
pca_scores = pca.fit_transform(X_scaled)

k_results = []
for k in range(2, 9):
    model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=20)
    labels = model.fit_predict(X_scaled)
    k_results.append({"k": k, "inertia": model.inertia_, "silhouette": silhouette_score(X_scaled, labels)})
k_evaluation = pd.DataFrame(k_results)
k_evaluation.to_csv(OUT / "cluster_k_evaluation.csv", index=False)
print("cluster_k_evaluation.csv:", k_evaluation.shape)

selected_k = 2
kmeans = KMeans(n_clusters=selected_k, random_state=RANDOM_STATE, n_init=20)
cluster_labels = kmeans.fit_predict(X_scaled)

cluster_assignments = pd.DataFrame({"Region": cluster_features.index, "Cluster": cluster_labels}).set_index("Region")

cluster_profile = (
    cluster_features.join(cluster_assignments)
    .groupby("Cluster")[feature_cols]
    .mean()
    .reset_index()
)
cluster_profile.to_csv(OUT / "cluster_profiles.csv", index=False)
print("cluster_profiles.csv:", cluster_profile.shape)

cluster_membership = cluster_assignments.reset_index().sort_values(["Cluster", "Region"])
cluster_membership.to_csv(OUT / "cluster_membership.csv", index=False)
print("cluster_membership.csv:", cluster_membership.shape)

pca_2d = pd.DataFrame(
    pca_scores[:, :2], columns=["PC1", "PC2"], index=cluster_features.index
).reset_index().rename(columns={"index": "Region"})
pca_2d.to_csv(OUT / "pca_region_scores.csv", index=False)
print("pca_region_scores.csv:", pca_2d.shape)

# ------------------------------------------------------------
# 7. Anomaly detection (IQR + rolling z-score)
# ------------------------------------------------------------
anomaly_parts = []
for (region, area), group in clean_df.groupby(["Region", "Area"]):
    group = group.sort_values("Date").copy()
    values = group[UNEMP]
    q1, q3 = values.quantile(0.25), values.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    group["IQR_Anomaly"] = (values < lower) | (values > upper)

    rolling_mean = values.shift(1).rolling(window=3, min_periods=2).mean()
    rolling_std = values.shift(1).rolling(window=3, min_periods=2).std()
    group["Rolling_Z"] = (values - rolling_mean) / rolling_std.replace(0, np.nan)
    group["Rolling_Z_Anomaly"] = group["Rolling_Z"].abs() >= 3
    group["Any_Anomaly"] = group["IQR_Anomaly"] | group["Rolling_Z_Anomaly"]
    anomaly_parts.append(group)

anomaly_df = pd.concat(anomaly_parts, ignore_index=True)

def classify_anomaly(row):
    if not row["Any_Anomaly"]:
        return "Not flagged"
    value = row[UNEMP]
    if value < 0 or value > 100:
        return "Data-quality anomaly"
    if row["Date"] in [pd.Timestamp("2020-04-30"), pd.Timestamp("2020-05-31")]:
        return "Legitimate COVID extreme event"
    if pd.Timestamp("2020-03-01") <= row["Date"] <= pd.Timestamp("2020-06-30"):
        return "COVID-period noteworthy anomaly"
    return "Noteworthy / unexplained"

anomaly_df["Anomaly_Category"] = anomaly_df.apply(classify_anomaly, axis=1)

anomaly_log = anomaly_df[anomaly_df["Any_Anomaly"]][
    ["Region", "Area", "Date", UNEMP, "IQR_Anomaly", "Rolling_Z", "Rolling_Z_Anomaly", "Anomaly_Category"]
].sort_values("Date")
anomaly_log.to_csv(OUT / "anomaly_log.csv", index=False)
print("anomaly_log.csv:", anomaly_log.shape)

# ------------------------------------------------------------
# 8. Forecasting (rolling-origin one-step benchmarks)
# ------------------------------------------------------------
national_series = clean_df.groupby("Date")[UNEMP].mean().sort_index()

def forecast_one(model_name, train):
    if model_name == "Naive":
        return float(train.iloc[-1])
    if model_name == "Drift":
        if len(train) < 2:
            return float(train.iloc[-1])
        slope = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
        return float(train.iloc[-1] + slope)
    if model_name == "SES":
        model = SimpleExpSmoothing(train, initialization_method="estimated").fit(optimized=True)
        return float(model.forecast(1).iloc[0])
    if model_name == "Holt":
        model = Holt(train, initialization_method="estimated").fit(optimized=True)
        return float(model.forecast(1).iloc[0])
    if model_name == "AR1":
        model = AutoReg(train, lags=1, trend="c").fit()
        return float(model.predict(start=len(train), end=len(train)).iloc[0])
    if model_name == "AR2":
        if len(train) < 5:
            raise ValueError("AR2 requires more training observations.")
        model = AutoReg(train, lags=2, trend="c").fit()
        return float(model.predict(start=len(train), end=len(train)).iloc[0])
    if model_name == "ARIMA":
        model = ARIMA(train, order=(1, 1, 0)).fit()
        return float(model.forecast(1).iloc[0])
    raise ValueError(f"Unknown model: {model_name}")

models = ["Naive", "Drift", "SES", "Holt", "AR1", "AR2", "ARIMA"]
model_display = {
    "Naive": "Naive", "Drift": "Drift", "SES": "Simple Exponential Smoothing",
    "Holt": "Holt Linear", "AR1": "AR(1)", "AR2": "AR(2)", "ARIMA": "ARIMA(1,1,0)",
}

initial_train = 8
forecast_records = []
for i in range(initial_train, len(national_series)):
    train = national_series.iloc[:i]
    actual = float(national_series.iloc[i])
    test_date = national_series.index[i]
    for model_name in models:
        try:
            prediction = forecast_one(model_name, train)
        except Exception:
            prediction = np.nan
        forecast_records.append({"Date": test_date, "Model": model_name, "Actual": actual, "Forecast": prediction, "Error": actual - prediction})

forecast_values = pd.DataFrame(forecast_records)
forecast_values["Absolute_Error"] = forecast_values["Error"].abs()
forecast_values["Squared_Error"] = forecast_values["Error"] ** 2

forecast_metrics = (
    forecast_values.dropna().groupby("Model")
    .agg(MAE=("Absolute_Error", "mean"), RMSE=("Squared_Error", lambda x: np.sqrt(x.mean())), Mean_Error=("Error", "mean"), Test_Points=("Error", "size"))
    .sort_values("MAE").reset_index()
)
forecast_metrics["Model"] = forecast_metrics["Model"].map(model_display).fillna(forecast_metrics["Model"])
forecast_metrics.to_csv(OUT / "forecast_model_metrics.csv", index=False)
print("forecast_model_metrics.csv:", forecast_metrics.shape)

# Wide format for the Forecast vs Actual chart: one row per Test_Date
wide = forecast_values.pivot_table(index=["Date", "Actual"], columns="Model", values="Forecast").reset_index()
wide = wide.rename(columns={"Date": "Test_Date", **model_display})
ordered_cols = ["Test_Date", "Actual"] + [model_display[m] for m in models if model_display[m] in wide.columns]
wide = wide[ordered_cols].sort_values("Test_Date")
wide.insert(0, "Date", wide["Test_Date"])
wide.to_csv(OUT / "rolling_origin_forecast_values.csv", index=False)
print("rolling_origin_forecast_values.csv:", wide.shape)

# ------------------------------------------------------------
# 9. Key findings + limitations
# ------------------------------------------------------------
pre_mean = clean_df.loc[clean_df["Period"] == "Pre-COVID", UNEMP].mean()
covid_mean = clean_df.loc[clean_df["Period"] == "COVID", UNEMP].mean()
top_shock = regional_profile.sort_values("Shock_Magnitude_pp", ascending=False).iloc[0]

key_findings = pd.DataFrame([
    {"Finding_ID": "F1", "Theme": "National shock", "Finding": "Mean unemployment rose sharply during the COVID period.",
     "Evidence": f"Pre-COVID mean {pre_mean:.2f}% vs COVID mean {covid_mean:.2f}% ({covid_mean - pre_mean:+.2f} pp).",
     "Caveat": "National average masks regional heterogeneity."},
    {"Finding_ID": "F2", "Theme": "Regional heterogeneity", "Finding": "COVID shock magnitude varies substantially by region.",
     "Evidence": f"{top_shock['Region']} recorded the largest shock at {top_shock['Shock_Magnitude_pp']:+.2f} pp.",
     "Caveat": "Some regions have incomplete monthly coverage."},
    {"Finding_ID": "F3", "Theme": "Rural vs Urban", "Finding": "Rural/Urban differences are period-dependent.",
     "Evidence": "Balanced-region Mann-Whitney test was significant pre-COVID and not significant during COVID at the 5% level.",
     "Caveat": "Small effect sizes; not a causal claim."},
    {"Finding_ID": "F4", "Theme": "Coverage", "Finding": "Regional data coverage is uneven across the sample.",
     "Evidence": f"{len(fully_covered_regions)} regions fully covered; {len(incomplete_regions)} regions incomplete.",
     "Caveat": "Descriptive coverage audit, not a data-quality defect."},
    {"Finding_ID": "F5", "Theme": "Forecasting", "Finding": "Simple benchmark models are competitive on this short series.",
     "Evidence": f"Best model by MAE: {forecast_metrics.iloc[0]['Model']} ({forecast_metrics.iloc[0]['MAE']:.3f} pp).",
     "Caveat": "14-month series with a structural COVID shock; not a long-horizon forecast."},
])
key_findings.to_csv(OUT / "phase10_key_findings.csv", index=False)
print("phase10_key_findings.csv:", key_findings.shape)

limitations = pd.DataFrame([
    {"ID": "L1", "Limitation": "Short time window", "Evidence": "Only 14 monthly observations are available.", "Implication": "Limits time-series inference and long-horizon forecasting."},
    {"ID": "L2", "Limitation": "Uneven regional coverage", "Evidence": f"{len(fully_covered_regions)} regions fully covered; {len(incomplete_regions)} incomplete.", "Implication": "Cross-regional comparisons should note coverage status."},
    {"ID": "L3", "Limitation": "COVID structural shock", "Evidence": "The COVID period dominates variance in the series.", "Implication": "Should not be treated as ordinary seasonality."},
    {"ID": "L4", "Limitation": "No causal claims", "Evidence": "Tests are correlational / distributional comparisons.", "Implication": "Findings support association, not causation."},
    {"ID": "L5", "Limitation": "Small clustering sample", "Evidence": "Only 28 regions are available for clustering.", "Implication": "Cluster interpretation should remain descriptive."},
])
limitations.to_csv(OUT / "phase10_limitations.csv", index=False)
print("phase10_limitations.csv:", limitations.shape)

print("\nAll data files written to", OUT)
