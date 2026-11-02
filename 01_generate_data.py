import numpy as np
import pandas as pd

np.random.seed(42)
N = 5000

credit_score = np.random.normal(loc=680, scale=60, size=N).clip(300, 850).astype(int)

dealer_id = np.random.choice([f"D{i:03d}" for i in range(1, 16)], size=N)
dealer_risk_multiplier = {f"D{i:03d}": np.random.uniform(0.7, 1.4) for i in range(1, 16)}

loan_amount = np.round(np.random.gamma(shape=6, scale=3200, size=N) + 8000, -2)
loan_amount = loan_amount.clip(8000, 45000)

loan_term_months = np.random.choice([36, 48, 60, 72], size=N, p=[0.15, 0.25, 0.40, 0.20])

base_rate = 18 - (credit_score - 300) / (850 - 300) * 14
interest_rate = np.round(base_rate + np.random.normal(0, 1.2, N), 2).clip(3.5, 24.9)

print("Sample of generated fields so far:")
df_preview = pd.DataFrame({
    "credit_score": credit_score,
    "dealer_id": dealer_id,
    "loan_amount": loan_amount,
    "loan_term_months": loan_term_months,
    "interest_rate": interest_rate,
})
print(df_preview.head(10))

approval_score = (credit_score - 500) / 350
approval_prob = 1 / (1 + np.exp(-6 * (approval_score - 0.4)))
approved = np.random.binomial(1, approval_prob)

print(f"\nOverall approval rate: {approved.mean():.1%}")

temp = pd.DataFrame({"credit_score": credit_score, "approved": approved})
temp["band"] = pd.cut(temp["credit_score"], bins=[300, 580, 640, 700, 760, 851], right=False, labels=["300-579", "580-639", "640-699", "700-759", "760-850"])
print("\nApproval rate by credit score band:")
print(temp.groupby("band", observed=True)["approved"].mean())

base_default_prob = (850 - credit_score) / 550 * 0.35
term_factor = (loan_term_months - 36) / 36 * 0.05
rate_factor = (interest_rate - 5) / 20 * 0.08
dealer_factor = np.array([dealer_risk_multiplier[d] for d in dealer_id])

default_prob = (base_default_prob + term_factor + rate_factor) * dealer_factor
default_prob = np.clip(default_prob, 0.01, 0.85)

defaulted = np.where(
    approved == 1,
    np.random.binomial(1, default_prob),
    0
)

print(f"\nOverall default rate (among approved loans): {defaulted[approved==1].mean():.1%}")

temp2 = pd.DataFrame({"credit_score": credit_score, "approved": approved, "defaulted": defaulted})
temp2 = temp2[temp2["approved"] == 1]
temp2["band"] = pd.cut(temp2["credit_score"], bins=[300, 580, 640, 700, 760, 851], right=False, labels=["300-579", "580-639", "640-699", "700-759", "760-850"])
print("\nDefault rate by credit score band (approved loans only):")
print(temp2.groupby("band", observed=True)["defaulted"].mean())

loan_id = [f"L{i:05d}" for i in range(1, N + 1)]

application_date = pd.to_datetime("2024-01-01") + pd.to_timedelta(
    np.random.randint(0, 730, N), unit="D"
)

df = pd.DataFrame({
    "loan_id": loan_id,
    "application_date": application_date,
    "dealer_id": dealer_id,
    "credit_score": credit_score,
    "loan_amount": loan_amount,
    "loan_term_months": loan_term_months,
    "interest_rate": interest_rate,
    "approved": approved,
    "defaulted": defaulted,
})

messy_df = df.copy()

missing_idx = np.random.choice(messy_df.index, size=int(N * 0.02), replace=False)
messy_df.loc[missing_idx, "loan_amount"] = np.nan

dupe_rows = messy_df.sample(15, random_state=1)
messy_df = pd.concat([messy_df, dupe_rows], ignore_index=True)

output_path = "auto_loan_data.csv"
messy_df.to_csv(output_path, index=False)

print(f"\nFinal dataset saved: {output_path}")
print(f"Total rows (including {len(dupe_rows)} intentional duplicates): {len(messy_df)}")
print(f"Missing loan_amount values (intentional): {messy_df['loan_amount'].isna().sum()}")
print("\nFirst 5 rows of final dataset:")
print(messy_df.head())
