# 🇮🇳 India Unemployment Analytics

## A Regional Diagnostic of India's Unemployment Before and During COVID-19

**May 2019 – June 2020**

A complete end-to-end data analysis project covering data cleaning, quality auditing, EDA, statistical analysis, regional profiling, clustering, anomaly detection, time-series diagnostics, scoped forecasting, insight synthesis, an interactive Streamlit dashboard, a final report, and a reproducible Jupyter Notebook.

---

## 📌 Project Overview

This project analyzes unemployment in India from **May 2019 to June 2020**, focusing on the change before and during the COVID-19 period and the differences across Indian regions.

### Main Questions

- How did unemployment change from Pre-COVID to COVID?
- How large was the unemployment shock?
- How different were regional responses?
- How did Rural and Urban unemployment compare?
- What relationships exist between unemployment, employment, and labour participation?
- Which observations were identified as anomalies?
- Do regions form distinct unemployment profiles?
- What time-series behavior can be identified?
- How useful are short-horizon forecasting benchmarks?

> This is an observational analysis. Statistical association does not establish causation.

---

## 📊 Dataset

| Attribute | Value |
|---|---:|
| Time period | May 2019 – June 2020 |
| Monthly dates | 14 |
| Regions | 28 |
| Areas | 2 |
| Clean observations | 740 |
| Fully covered regions | 20 |
| Incomplete regions | 8 |

### Main Variables

- `Region`
- `Date`
- `Frequency`
- `Estimated Unemployment Rate (%)`
- `Estimated Employed`
- `Estimated Labour Participation Rate (%)`
- `Area`
- `Period`

### Analytical Periods

- **Pre-COVID:** May 2019 – February 2020
- **COVID:** March 2020 – June 2020

---

# 🧭 Project Pipeline

```text
Raw Dataset
    ↓
Phase 1 — Cleaning & Validation
    ↓
Phase 2 — Data Dictionary & Coverage Audit
    ↓
Phase 3 — Exploratory Data Analysis
    ↓
Phase 4 — Statistical Analysis
    ↓
Phase 5 — Regional Profiling
    ↓
Phase 6 — PCA & K-Means Clustering
    ↓
Phase 7 — Anomaly Detection
    ↓
Phase 8 — Time-Series Diagnostics
    ↓
Phase 9 — Scoped Forecasting
    ↓
Phase 10 — Insight Synthesis
    ├── Phase 11 — Interactive Dashboard
    └── Phase 12 — Final Report
             ↓
    Phase 13 — Complete Jupyter Notebook
```

---

# 🔬 Project Phases

### Phase 1 — Data Cleaning & Validation
- Removed fully blank rows
- Standardized column names and text
- Converted dates and numeric variables
- Validated duplicates and numeric ranges
- Created Pre-COVID/COVID periods

### Phase 2 — Data Dictionary & Coverage Audit
Documents variable definitions, monthly coverage, missing Region-Area-Month combinations, and analysis eligibility.

### Phase 3 — Exploratory Data Analysis
Includes national trends, distributions, regional analysis, Rural vs Urban comparisons, employment, labour participation, and correlations.

### Phase 4 — Statistical Analysis
Includes:
- Pearson and Spearman correlations
- Mann-Whitney U tests
- Rank-biserial effect size
- Kruskal-Wallis tests
- Epsilon-squared effect size

### Phase 5 — Regional Profiling
Profiles regions by baseline, COVID shock, volatility, trends, peak, June 2020 level, recovery gap, and coverage.

### Phase 6 — PCA & K-Means
Uses standardized regional features, PCA, elbow diagnostics, silhouette scores, and K-Means. The selected descriptive solution is **k = 2**.

### Phase 7 — Anomaly Detection
Uses IQR and trailing rolling z-score detection. COVID-period extremes are classified contextually rather than automatically deleted.

### Phase 8 — Time-Series Diagnostics
Includes ADF, KPSS, first differences, ACF, PACF, and month-to-month shock diagnostics.

### Phase 9 — Scoped Forecasting
Evaluates Naive, Drift, SES, Holt, AR(1), AR(2), and ARIMA(1,1,0) using rolling-origin one-step-ahead validation.

### Phase 10 — Insight Synthesis
Integrates evidence into key findings, regional shock synthesis, cluster synthesis, dashboard KPIs, and limitations.

---

# 📊 Phase 11 — Interactive Dashboard

The project includes a Streamlit dashboard with an India-inspired visual identity:

- 🇮🇳 Indian tricolor visual language
- Deep emerald green
- Saffron/orange
- Navy
- White analytical cards
- India landmarks and map
- Custom KPI and section icons
- Sidebar navigation

### Dashboard Sections

- Overview
- National Trends
- Regional Analysis
- Rural vs Urban
- Statistical Tests
- Clustering
- Anomaly Detection
- Forecasting
- Key Insights
- Data Explorer
- Limitations

### Run

```bash
cd Unemployment_India_Phase11_Dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

# 📑 Phase 12 — Final Report

The final report contains:

- Executive Summary
- Methodology
- Data Quality
- EDA
- Statistical Evidence
- Regional Analysis
- Clustering
- Anomaly Detection
- Time-Series Diagnostics
- Forecasting
- Key Findings
- Limitations
- Final Conclusions

---

# 📓 Phase 13 — Complete Jupyter Notebook

The complete project is consolidated into:

```text
Unemployment_India_Phase13_Notebook/
└── India_Unemployment_Complete_Project_Phase13.ipynb
```

Run it with:

```bash
cd Unemployment_India_Phase13_Notebook
pip install -r requirements.txt
jupyter notebook
```

The notebook uses:

```text
data/Unemployment in India(1).csv
```

and is designed to execute from top to bottom.

---

# 📁 Repository Structure

```text
India-Unemployment-Analytics/
│
├── Unemployment_India_Phase1/
├── Unemployment_India_Phase2/
├── Unemployment_India_Phase3/
├── Unemployment_India_Phase4/
├── Unemployment_India_Phase5/
├── Unemployment_India_Phase6/
├── Unemployment_India_Phase7/
├── Unemployment_India_Phase8/
├── Unemployment_India_Phase9/
├── Unemployment_India_Phase10/
│
├── Unemployment_India_Phase11_Dashboard/
│   ├── app.py
│   ├── README.md
│   ├── requirements.txt
│   └── data/
│
├── Unemployment_India_Phase12_Final_Report/
│   ├── Final_Report.md
│   ├── final_executive_summary.csv
│   ├── final_findings.csv
│   ├── final_methodology.csv
│   └── figures/
│
└── Unemployment_India_Phase13_Notebook/
    ├── India_Unemployment_Complete_Project_Phase13.ipynb
    ├── README.md
    ├── requirements.txt
    └── data/
        └── Unemployment in India(1).csv
```

---

# 📈 Key Findings

- **740** cleaned observations across **28 regions**.
- **20 regions** have complete monthly coverage.
- National unemployment increased substantially during COVID-19.
- The national unemployment peak occurred in **May 2020**.
- Regional shock magnitudes varied considerably.
- Rural/Urban differences were statistically significant before COVID but not in the balanced COVID comparison at the 5% level.
- Regional heterogeneity was statistically significant in both periods.
- COVID-period observations formed a major concentration of detected anomalies.
- No hard out-of-range data-quality anomalies were identified.
- PCA and K-Means revealed descriptive regional structure.
- Forecasting is constrained by the short 14-month series and the COVID structural break.

---

# ⚠️ Limitations

1. Only 14 monthly observations are available.
2. COVID represents a major structural shock.
3. Eight regions have incomplete coverage.
4. Only 28 regions are available for clustering.
5. One cluster contains only four regions.
6. Observational data cannot establish causation.
7. Forecasting has very few validation points and is intended as a benchmark only.

---

# 🛠️ Technologies

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- Scikit-learn
- Statsmodels
- Streamlit
- Jupyter Notebook

### Analytical Methods

Data Cleaning · EDA · Correlation Analysis · Mann-Whitney U · Kruskal-Wallis · PCA · K-Means · IQR Anomaly Detection · Rolling Z-Score · ADF · KPSS · ACF · PACF · Rolling-Origin Forecasting · MAE · RMSE

---

# 👩‍💻 Author

<div align="center">

## Noura Maher Elamin

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://www.linkedin.com/in/nouramaherelamin/)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/nouramaherelamin)

</div>

---

# 📌 Final Analytical Message

**India experienced a substantial unemployment shock during COVID-19, with strong regional heterogeneity. The dataset supports descriptive and statistical analysis of this shock, while its short time span limits causal inference and long-horizon forecasting.**
