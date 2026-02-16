# A/B Testing & Causal Impact — Loan Application Flow Experiment

## Live Dashboard

🔗 Streamlit App: https://ab-testing-causal-impact-mrdd3ocmui6m7uhxh3tngz.streamlit.app/

Overview

This project analyzes a randomized A/B experiment evaluating a simplified loan application flow (5 steps → 3 steps).

Baseline conversion: ~8%
Experiment duration: 14 days
Target MDE: +1 percentage point

The goal was to determine whether reducing friction increases completion rates while maintaining experimental integrity.

Key Findings

Steady-state uplift: +1.25 percentage points

Statistically significant improvement: p < 0.001

Non-overlapping 95% confidence intervals

Estimated impact: ~3,739 additional completed applications per month

Estimated revenue impact: ~4.49M per month

However:

Sample Ratio Mismatch (SRM) detected (60/40 split instead of expected 50/50)

Allocation imbalance introduces potential bias

Final Recommendation

Do not immediately ship.

Recommended next steps:

Investigate and correct traffic allocation logic

Rerun the experiment under proper 50/50 randomization

Validate uplift stability before rollout

If uplift remains consistent under corrected allocation, proceed with rollout.

Skills Demonstrated

Randomized experiment design

Sample Ratio Mismatch (SRM) detection

Two-proportion z-test for uplift estimation

95% Wilson confidence intervals

Novelty effect analysis

Difference-in-Differences (DiD) causal framing

Financial impact quantification

Project Structure
fintech_ab_test/
├── generate_data.py
├── experiment_data.csv
├── notebooks/
│   └── ab_analysis.ipynb
└── README.md