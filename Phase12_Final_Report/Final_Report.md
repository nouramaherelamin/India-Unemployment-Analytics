# Labour Market Shockwaves
## A Regional Diagnostic of India's Unemployment Before and During COVID-19
### Final Report — Phases 1–12

---

## Executive Summary

This project analyzes India's unemployment patterns from **May 2019 through June 2020**, using the uploaded unemployment dataset after structured cleaning and validation.

The final cleaned analytical dataset contains **740 observations**, covering **28 regions**, **2 areas (Rural and Urban)**, and **14 monthly dates**.

The central descriptive finding is a substantial increase in national unemployment during the COVID period:

- **Pre-COVID mean:** 9.508%
- **COVID mean:** 17.780%
- **Absolute change:** +8.272 percentage points
- **Relative change:** +86.997%

The national monthly mean reached an observed peak of **24.875% in 2020-05-31**.

The analysis also shows substantial regional heterogeneity. The largest observed positive regional change was **Puducherry (+37.362 pp)**, while the smallest observed change was **Jammu & Kashmir (-4.332 pp)**.

Statistical testing indicates strong regional distributional differences in both periods. Rural and Urban unemployment distributions differed significantly before COVID in the balanced-region analysis, while the COVID-period balanced comparison was not statistically significant at the 5% threshold.

The anomaly analysis found a strong concentration of extreme flags around the COVID shock, with **0 hard data-quality anomalies** detected.

The time-series and forecasting sections are intentionally scoped. There are only **14 monthly observations**, with the final four months containing an exceptional structural shock. Therefore, forecasting results are treated as benchmark diagnostics rather than long-term predictions.

---

# 1. Project Objectives

The project was designed to answer five broad questions:

1. How did unemployment change between the Pre-COVID and COVID periods?
2. How heterogeneous were the effects across regions?
3. Did Rural and Urban unemployment distributions differ?
4. What statistical and time-series patterns can be supported by the available data?
5. Can the cleaned dataset support useful segmentation, anomaly detection, and short-horizon forecasting diagnostics?

The analysis was organized into 12 phases, from data cleaning through dashboard and final reporting.

---

# 2. Dataset and Data Quality

## 2.1 Raw Dataset

The raw dataset contained:

- **768 rows**
- **7 columns**
- Monthly unemployment observations across Indian regions and areas.

The raw file contained **28 fully blank trailing rows**.

After removing only those fully blank rows and normalizing fields, the cleaned dataset contained:

- **740 rows**
- **8 analytical columns**, including the derived period field
- **28 regions**
- **2 areas**
- **1 frequency: Monthly**
- Date range: **31-May-2019 to 30-Jun-2020**

## 2.2 Validation

The cleaning and validation phase found:

- Date parsing failures: **0**
- Duplicate Region-Date-Area combinations: **0**
- Unemployment values outside [0,100]: **0**
- Labour participation values outside [0,100]: **0**
- Negative employment values: **0**
- Missing values inside the cleaned analytical dataset: **0**

The extreme unemployment observations in April–May 2020 were retained because they represent legitimate observations in the shock period rather than automatically being treated as data errors.

## 2.3 Regional Coverage

The dataset contains **20 fully covered regions** and **8 incomplete regions**.

Incomplete regions:

Assam, Chandigarh, Goa, Jammu & Kashmir, Meghalaya, Puducherry, Sikkim, Uttarakhand

For regional statistical comparisons requiring balanced monthly coverage, the project therefore uses the **20 fully covered regions**.

---

# 3. Analytical Framework

The project used:

### Descriptive Analysis
- Mean
- Median
- Standard deviation
- IQR
- Distribution shape
- Monthly trend
- Pre-COVID vs COVID comparison

### Statistical Testing
- Pearson correlation
- Spearman correlation
- Mann-Whitney U
- Kruskal-Wallis
- Effect sizes

### Regional Analysis
- Baseline unemployment
- COVID shock magnitude
- Volatility
- Trend slope
- Peak month
- Recovery indicators

### Segmentation
- Standardization
- PCA
- K-Means
- Silhouette and elbow diagnostics

### Anomaly Detection
- IQR
- Trailing 3-month rolling z-score
- Event-context classification

### Time-Series Diagnostics
- ADF
- KPSS
- ACF
- PACF
- First differences

### Forecasting
- Naive
- Drift
- Simple Exponential Smoothing
- Holt Linear
- AR(1)
- AR(2)
- ARIMA(1,1,0)
- Rolling-origin one-step-ahead evaluation

---

# 4. National Unemployment Findings

## 4.1 Pre-COVID vs COVID

| Period | Mean Unemployment |
|---|---:|
| Pre-COVID | 9.508% |
| COVID | 17.780% |

The observed change was:

**+8.272 percentage points (+86.997%)**

The national monthly peak was:

**24.875% — 2020-05-31**

The lowest observed national monthly mean was:

**8.874% — 2019-05-31**

The largest month-to-month movements occurred during the COVID period, including a sharp increase in April 2020 and a sharp decrease in June 2020.

This pattern is consistent with a large shock followed by a partial reversal within the limited observation window.

---

# 5. Regional Heterogeneity

Regional analysis shows that national averages conceal substantial differences between regions.

The largest observed regional shock was:

**Puducherry: +37.362 percentage points**

The smallest observed regional change was:

**Jammu & Kashmir: -4.332 percentage points**

The largest positive shock values included:

- **Puducherry:** +37.362 pp
- **Tamil Nadu:** +22.567 pp
- **Jharkhand:** +22.069 pp
- **Bihar:** +17.798 pp
- **Karnataka:** +12.046 pp
- **Haryana:** +11.717 pp
- **Kerala:** +10.960 pp
- **Telangana:** +10.787 pp
- **Madhya Pradesh:** +9.329 pp
- **Andhra Pradesh:** +8.539 pp

Because some regions have incomplete coverage, regional comparisons should distinguish between fully covered and incomplete regions.

The analysis does not label a region as "best" or "worst"; the regional metrics are descriptive measures of baseline, shock, volatility, and recovery.

---

# 6. Rural vs Urban Analysis

The Rural and Urban areas were analyzed both overall and using the balanced-region subset.

For the balanced 20-region comparison:

### Pre-COVID
- Mann-Whitney U: statistically significant
- p = **0.00039**
- Rank-biserial effect size: approximately **-0.205**
- Effect size: small

### COVID
- Mann-Whitney U: not statistically significant at 5%
- p = **0.14983**
- Rank-biserial effect size: approximately **-0.132**
- Effect size: small

### Interpretation

The data support a distributional difference between Rural and Urban unemployment before COVID in the balanced-region sample.

During the COVID period, the corresponding balanced-region test did not provide sufficient evidence of a statistically significant difference at the 5% threshold.

These results are distributional comparisons and do not establish why the groups differed or whether one variable caused another.

---

# 7. Regional Statistical Heterogeneity

Kruskal-Wallis testing across the 20 fully covered regions found statistically significant differences in both periods:

- **Pre-COVID: p < 0.001**
- **COVID: p = 0.00108**

The reported epsilon-squared effect sizes were large:

- Pre-COVID: approximately **0.805**
- COVID: approximately **0.175**

This provides strong evidence that regional unemployment distributions are an important part of the dataset structure.

---

# 8. Correlation Analysis

## 8.1 Unemployment vs Labour Participation

Overall Spearman correlation:

**rho = -0.02357**

This indicates a very weak overall monotonic relationship.

Period-specific Spearman correlations:

- Pre-COVID: **rho = 0.09854**
- COVID: **rho = -0.07635**

The direction differed between periods, reinforcing the importance of separating the shock period from the baseline period.

## 8.2 Unemployment vs Estimated Employment

Overall Spearman correlation:

**rho = -0.21659**

The relationship was negative.

However, correlation in observational data does not establish a causal relationship. Regional scale, timing, labour-market composition, and the structure of the recorded variables may all contribute to the observed association.

---

# 9. Regional Profiling

The regional profiling phase created a descriptive profile for every region using:

- Coverage status
- Pre-COVID mean
- COVID mean
- Median
- Volatility
- Coefficient of variation
- Trend slope
- Peak month
- Shock magnitude
- June 2020 level
- Recovery indicators

Important observations included:

- **20 regions** had complete Rural and Urban monthly coverage.
- **8 regions** had incomplete coverage.
- **Puducherry** had the largest observed positive shock.
- **Jammu & Kashmir** had the smallest observed shock.
- Some regions returned to or below their Pre-COVID baseline by June 2020, while others remained above baseline.

These are descriptive profiles rather than performance rankings.

---

# 10. Regional Clustering

Phase 6 used seven standardized regional features:

- Pre-COVID mean unemployment
- COVID mean unemployment
- Shock magnitude
- Volatility
- Trend slope
- Pre-COVID participation
- COVID participation

PCA showed:

- PC1: approximately **50.66%**
- PC2: approximately **25.06%**
- PC1 + PC2: approximately **75.72%**

K-Means evaluation selected:

**k = 2**

Cluster sizes:

- Cluster 0: **24 regions**
- Cluster 1: **4 regions**

The four-region cluster contained:

**Bihar, Jharkhand, Puducherry, Tamil Nadu**

### Caution

The clustering sample contains only 28 regions, and one cluster contains only four regions. Therefore, the clusters should be treated as descriptive segmentation rather than stable population classes.

---

# 11. Anomaly Detection

Phase 7 used two complementary methods:

1. IQR rule within each Region-Area series
2. Trailing 3-month rolling z-score

Results:

- IQR flags: **93**
- Rolling z-score flags: **127**
- Unique flagged observations: **173**

Classification:

| Category | Count |
|---|---:|
| Legitimate COVID extreme event | 79 |
| COVID-period noteworthy anomaly | 23 |
| Noteworthy / unexplained | 71 |
| Data-quality anomaly | 0 |

The strong concentration of anomaly flags in April–May 2020 is consistent with the major COVID shock visible in the national series.

Importantly, **"Noteworthy / unexplained" does not mean incorrect**. It means the dataset itself does not provide enough contextual information to attribute the observation to a particular event.

---

# 12. Time-Series Diagnostics

The national time series contains only:

**14 monthly observations**

This is a major limitation.

## Stationarity

ADF level test:

**p = 0.99899**

KPSS level test:

**p = 0.07564**

The tests do not provide a fully concordant conclusion.

The ACF showed:

- Lag 1: approximately **0.524**
- Later lags: substantially smaller

The short sample and COVID structural break mean that ACF/PACF and stationarity diagnostics should be interpreted as exploratory rather than definitive.

Annual seasonality cannot be reliably estimated from only 14 months.

---

# 13. Forecasting

Forecasting was deliberately scoped to one-step-ahead rolling-origin backtesting.

Models tested:

- Naive
- Drift
- Simple Exponential Smoothing
- Holt Linear
- AR(1)
- AR(2)
- ARIMA(1,1,0)

Overall results:

| Model | MAE |
|---|---:|
| Drift | 4.712 |
| Naive | 4.725 |
| Simple Exponential Smoothing | 4.825 |
| Holt Linear | 6.654 |
| ARIMA(1,1,0) | 11.332 |
| AR(1) | 15.702 |
| AR(2) | 24.668 |

The lowest observed backtesting MAE was obtained by:

**Drift: 4.712 percentage points**

The Naive benchmark had:

**4.725 percentage points**

For COVID-period test points:

**Drift: 6.947 percentage points**

### Forecasting limitation

Each model had only six rolling-origin test points.

Additionally:

- the series has only 14 months;
- there is a large structural break;
- no annual seasonality can be estimated reliably.

Therefore, these results are benchmark diagnostics and should not be presented as evidence of a robust long-term forecasting model.

---

# 14. Dashboard

Phase 11 produced a Streamlit dashboard containing:

1. National unemployment trend
2. Pre-COVID vs COVID comparison
3. Rural vs Urban trend
4. Regional COVID shock
5. Regional baseline vs shock
6. Anomaly detection
7. Regional clustering
8. Forecast benchmark
9. Statistical evidence
10. Limitations

The dashboard includes filters for:

- Region
- Area
- Period
- Date range

Observed and forecasted values are kept conceptually separate.

---

# 15. Key Analytical Findings

## Finding 1 — Large national shock

The mean unemployment rate increased from **9.508%** to **17.780%**, representing **+8.272 pp**.

## Finding 2 — Strong regional heterogeneity

Regional unemployment distributions differed significantly in both periods.

## Finding 3 — Rural/Urban differences were period-dependent

The balanced-region Rural/Urban comparison was significant before COVID but not significant during COVID at the 5% threshold.

## Finding 4 — Participation was weakly related to unemployment overall

The overall Spearman correlation was only **-0.02357**.

## Finding 5 — Extreme observations concentrated around COVID

The anomaly analysis identified a large concentration of extreme flags during the COVID shock, while detecting no hard data-quality anomalies.

## Finding 6 — Forecasting remains highly constrained

The dataset supports short-horizon benchmark comparison, not reliable long-horizon prediction.

---

# 16. Limitations

### 16.1 Short time series

Only 14 monthly observations are available.

### 16.2 Structural shock

The March–June 2020 period contains a major shock that changes the statistical structure of the series.

### 16.3 Incomplete regional coverage

8 regions do not have complete monthly coverage.

### 16.4 Small clustering sample

Only 28 regions are available, with one cluster containing only four regions.

### 16.5 Observational analysis

Correlation and distributional tests do not establish causal mechanisms.

### 16.6 Forecast validation size

Only six rolling-origin test points are available for each forecasting model.

### 16.7 Anomaly attribution

Some observations are flagged as noteworthy/unexplained because the dataset alone does not provide enough contextual information to explain them.

---

# 17. Recommended Dashboard Narrative

The dashboard should present the analysis in this sequence:

**National shock → Regional heterogeneity → Rural/Urban → Anomalies → Statistical evidence → Clustering → Forecasting limitations**

This order keeps the strongest descriptive evidence first and prevents the forecasting section from being interpreted as the primary result.

---

# 18. Final Conclusion

The analysis supports a clear descriptive conclusion:

**India's recorded unemployment rate experienced a large increase during the COVID period, while the magnitude and pattern of change varied substantially across regions.**

The strongest evidence comes from:

- National descriptive statistics
- Regional profiles
- Mann-Whitney comparisons
- Kruskal-Wallis testing
- Anomaly concentration
- Regional segmentation

The forecasting analysis provides useful methodological benchmarking, but the short time series and COVID structural break make long-term prediction inappropriate from this dataset alone.

The final analytical product should therefore emphasize **shock measurement, regional heterogeneity, statistical evidence, anomaly interpretation, and transparent limitations**, while presenting forecasting as a scoped diagnostic rather than a definitive prediction.

---

# 19. Project Deliverables

The project now contains:

- Phase 1 — Cleaning & Validation
- Phase 2 — Data Dictionary & Coverage Audit
- Phase 3 — Exploratory Data Analysis
- Phase 4 — Statistical Tests
- Phase 5 — Regional Profiling
- Phase 6 — Clustering
- Phase 7 — Anomaly Detection
- Phase 8 — Time-Series Diagnostics
- Phase 9 — Scoped Forecasting
- Phase 10 — Insight Synthesis
- Phase 11 — Interactive Dashboard
- Phase 12 — Final Report

---

## Final Project Status

**Analysis pipeline: COMPLETE**

**Dashboard: COMPLETE**

**Final report: COMPLETE**

**Main analytical limitation: 14-month time series with a major COVID structural shock**

**Primary analytical story: National shock + strong regional heterogeneity**
