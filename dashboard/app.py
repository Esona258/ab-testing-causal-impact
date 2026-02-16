import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chisquare
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

st.set_page_config(page_title="A/B Test Dashboard", layout="wide")

st.title("A/B Testing & Causal Impact — Loan Application Flow")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/experiment_data.csv")

df = load_data()

# --- SRM CHECK ---
st.header("1️⃣ Sample Ratio Mismatch (SRM)")

group_counts = df["group"].value_counts()
observed = group_counts.values
expected = [len(df) * 0.5, len(df) * 0.5]

stat, p_value_srm = chisquare(observed, expected)

col1, col2 = st.columns(2)
col1.metric("Control Share", f"{group_counts['control']/len(df):.2%}")
col2.metric("Treatment Share", f"{group_counts['treatment']/len(df):.2%}")

st.write("SRM p-value:", f"{p_value_srm:.6g}")

if p_value_srm < 0.01:
    st.error("SRM detected — allocation imbalance present.")
else:
    st.success("No SRM detected.")

# --- CONVERSION ---
st.header("2️⃣ Conversion Analysis")

conversion = df.groupby("group")["completed"].mean()

control = df[df.group == "control"]
treatment = df[df.group == "treatment"]

success = np.array([control.completed.sum(), treatment.completed.sum()])
nobs = np.array([len(control), len(treatment)])

z_stat, p_val = proportions_ztest(success, nobs)

uplift = conversion["treatment"] - conversion["control"]

col1, col2, col3 = st.columns(3)
col1.metric("Control Conversion", f"{conversion['control']:.2%}")
col2.metric("Treatment Conversion", f"{conversion['treatment']:.2%}")
col3.metric("Uplift", f"{uplift:.2%}")

st.write("Z-test p-value:", f"{p_val:.6g}")

# --- NOVELTY ---
st.header("3️⃣ Novelty Effect (Daily Trend)")

daily = df.groupby(["day", "group"])["completed"].mean().reset_index()

fig, ax = plt.subplots()
for g in ["control", "treatment"]:
    subset = daily[daily.group == g]
    ax.plot(subset.day, subset.completed, label=g)

ax.set_xlabel("Day")
ax.set_ylabel("Conversion Rate")
ax.legend()

st.pyplot(fig)

# --- BUSINESS IMPACT ---
st.header("4️⃣ Estimated Business Impact")

df_steady = df[df.day > 3]
conversion_steady = df_steady.groupby("group")["completed"].mean()
uplift_steady = conversion_steady["treatment"] - conversion_steady["control"]

monthly_apps = 300000
avg_revenue = 1200

extra_completions = monthly_apps * uplift_steady
incremental_revenue = extra_completions * avg_revenue

st.metric("Steady-State Uplift", f"{uplift_steady:.2%}")
st.metric("Estimated Monthly Revenue Impact", f"{incremental_revenue:,.0f}")

# --- FINAL DECISION ---
st.header("5️⃣ Recommendation")

if p_value_srm < 0.01:
    st.warning("Do NOT ship. Fix allocation and rerun experiment.")
else:
    if p_val < 0.05:
        st.success("Statistically significant uplift. Safe to consider rollout.")
    else:
        st.info("No significant uplift detected.")
