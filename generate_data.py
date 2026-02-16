import numpy as np
import pandas as pd

np.random.seed(42)

n_users = 100000
n_days = 14
baseline = 0.08
lift = 0.01
novelty_days = 3
novelty_extra = 0.008

# SRM bug: 60% control, 40% treatment
group = np.random.choice(["control", "treatment"], size=n_users, p=[0.6, 0.4])

day = np.random.randint(1, n_days + 1, size=n_users)

prob = np.full(n_users, baseline)

is_treatment = group == "treatment"
prob += is_treatment * lift
prob += (is_treatment & (day <= novelty_days)) * novelty_extra

prob = np.clip(prob, 0, 1)

completed = np.random.binomial(1, prob)

df = pd.DataFrame({
    "user_id": range(1, n_users + 1),
    "group": group,
    "day": day,
    "completed": completed
})

df.to_csv("experiment_data.csv", index=False)

print("Data generated successfully.")
