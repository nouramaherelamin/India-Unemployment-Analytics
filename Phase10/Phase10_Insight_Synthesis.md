# Labour Market Shockwaves
## Phase 10 — Insight Synthesis

### Executive Summary
The project covers Indian unemployment observations from **May 2019 to June 2020**. Mean unemployment increased from **9.510%** in the Pre-COVID period to **17.774%** during COVID, a change of **+8.264 percentage points (+86.898%)**.

The national monthly peak was **24.875% in 2020-05-31**. Regional variation was substantial: the largest observed regional change was **Puducherry (+37.362 pp)**, while the smallest was **Jammu & Kashmir (-4.332 pp)**.

### Core Findings
1. **National shock:** unemployment rose sharply during the COVID period.
2. **Peak:** the national series peaked in May 2020.
3. **Regional heterogeneity:** regional distributions differed strongly in both periods.
4. **Rural vs Urban:** the balanced-region test was significant before COVID but not significant during COVID.
5. **Participation:** unemployment and labour participation had a weak overall monotonic relationship.
6. **Employment:** unemployment and estimated employment had a negative overall association.
7. **Anomalies:** extreme flags concentrated around the COVID shock, with **0 data-quality anomalies**.
8. **Time series:** ADF and KPSS evidence was non-concordant; only 14 monthly observations are available.
9. **Forecasting:** simple benchmarks were more stable than higher-order autoregressive models in rolling-origin testing.
10. **Clustering:** k=2 was selected, but one cluster contains only four regions.

### Regional Shock Profile
Top observed positive changes:
- **Puducherry**: +37.362 pp
- **Tamil Nadu**: +22.567 pp
- **Jharkhand**: +22.069 pp
- **Bihar**: +17.798 pp
- **Karnataka**: +12.046 pp
- **Haryana**: +11.717 pp
- **Kerala**: +10.960 pp
- **Telangana**: +10.787 pp
- **Madhya Pradesh**: +9.329 pp
- **Andhra Pradesh**: +8.539 pp

Incomplete regions:
**Assam, Chandigarh, Goa, Jammu & Kashmir, Meghalaya, Puducherry, Sikkim, Uttarakhand**

Regional comparisons should prioritize the 20 fully covered regions where statistical analysis requires balanced monthly coverage.

### Statistical Evidence
- Balanced Rural vs Urban: pre-COVID **p=0.00039**; COVID **p=0.14983**.
- Kruskal-Wallis across fully covered regions: pre-COVID **p<0.001**; COVID **p=0.00108**.
- Overall Spearman unemployment vs participation: **rho=-0.02357**.
- Overall Spearman unemployment vs employment: **rho=-0.21659**.

These are observational statistical relationships and should not be presented as causal effects.

### Anomaly Synthesis
Phase 7 identified:
- **79** legitimate COVID extreme events
- **23** additional COVID-period noteworthy anomalies
- **71** noteworthy/unexplained anomalies
- **0** data-quality anomalies

“Noteworthy/unexplained” means the dataset alone does not provide enough context to attribute a specific event; it does not mean the observation is erroneous.

### Time-Series and Forecasting
The national series contains only 14 observations. Level stationarity tests were non-concordant:
- ADF p = **0.99899**
- KPSS p = **0.07564**

Forecasting used rolling-origin one-step-ahead evaluation. **Drift** had the lowest overall MAE (**4.712 pp**) and the Naive benchmark was close (**4.725 pp**). COVID-period best MAE was **6.947 pp** for **Drift**.

These results are diagnostic only: each model had six test origins, and the series has a major structural break.

### Limitations
- 14 monthly observations only.
- 4 COVID-period months contain a major structural shock.
- 8 regions have incomplete coverage.
- Clustering uses only 28 regions, with one cluster containing 4.
- Correlation and non-parametric tests do not establish causality.
- Forecast validation has only six test origins per model.
- Unexplained anomalies require external context for attribution.

### Phase 11 Dashboard Priorities
Recommended dashboard components:
- KPI cards for baseline, COVID mean, shock magnitude, peak, coverage.
- National monthly trend.
- Pre-COVID vs COVID comparison.
- Regional shock visualization.
- Rural vs Urban trend.
- Baseline-vs-shock regional scatter.
- Anomaly timeline.
- Cluster visualization.
- Clearly separated observed vs forecasted values.

### Final Analytical Message
The dataset supports a clear descriptive story of a **large national unemployment shock during COVID accompanied by strong regional heterogeneity**. The strongest evidence comes from descriptive analysis, regional statistical tests, and anomaly concentration around the COVID period.

The forecasting section should remain a **scoped benchmark**, not a long-term predictive claim, because the time series is too short and contains a major structural break.
