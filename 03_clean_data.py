import pandas as pd

# Load the raw messy data
df = pd.read_csv("auto_loan_data.csv")
required = {"loan_id", "application_date", "dealer_id", "credit_score", "loan_amount", "loan_term_months", "interest_rate", "approved", "defaulted"}
missing_columns = required - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
if df.empty:
    raise ValueError("Input contains no applications")
if df["dealer_id"].isna().any() or df["dealer_id"].astype(str).str.strip().eq("").any():
    raise ValueError("Missing dealer ID")

print(f"Starting row count: {len(df)}")

# --- Step 1: Check for missing values ---
print("\nMissing values per column:")
print(df.isna().sum())

# --- Step 2: Check for duplicate rows ---
# duplicated() flags rows that are exact repeats of an earlier row
num_duplicates = df.duplicated().sum()
print(f"\nNumber of exact duplicate rows found: {num_duplicates}")

# --- Step 3: Remove duplicates ---
df_clean = df.drop_duplicates().copy()
print(f"Row count after removing duplicates: {len(df_clean)}")

# --- Step 4: Handle missing loan_amount values ---
# Missing amounts are deliberately injected at random by the generator.
# Median imputation is an educational assumption, not a billing correction.
median_amount = df_clean["loan_amount"].median()
print(f"\nMedian loan amount (used to fill missing values): {median_amount}")

df_clean["loan_amount"] = df_clean["loan_amount"].fillna(median_amount)

print(f"Missing loan_amount values after cleaning: {df_clean['loan_amount'].isna().sum()}")

# Reject invalid records instead of silently publishing inconsistent metrics.
if not (df_clean["loan_id"].notna().all() and df_clean["loan_id"].is_unique):
    raise ValueError('Invalid input: df_clean["loan_id"].notna().all() and df_clean["loan_id"].is_unique')
if not (df_clean["credit_score"].between(300, 850).all()):
    raise ValueError('Invalid input: df_clean["credit_score"].between(300, 850).all()')
if not (df_clean["loan_amount"].gt(0).all()):
    raise ValueError('Invalid input: df_clean["loan_amount"].gt(0).all()')
if not (df_clean["loan_term_months"].isin([36, 48, 60, 72]).all()):
    raise ValueError('Invalid input: df_clean["loan_term_months"].isin([36, 48, 60, 72]).all()')
if not (df_clean["interest_rate"].between(0, 100).all()):
    raise ValueError('Invalid input: df_clean["interest_rate"].between(0, 100).all()')
if not (df_clean["approved"].isin([0, 1]).all()):
    raise ValueError('Invalid input: df_clean["approved"].isin([0, 1]).all()')
if not (df_clean["defaulted"].isin([0, 1]).all()):
    raise ValueError('Invalid input: df_clean["defaulted"].isin([0, 1]).all()')
if not ((df_clean["defaulted"] <= df_clean["approved"]).all()):
    raise ValueError('Invalid input: (df_clean["defaulted"] <= df_clean["approved"]).all()')
if not (pd.to_datetime(df_clean["application_date"], errors="coerce").notna().all()):
    raise ValueError('Invalid input: pd.to_datetime(df_clean["application_date"], errors="coerce").notna().all()')
from pathlib import Path
Path("reports").mkdir(exist_ok=True)
missing_unique = int(df.drop_duplicates()["loan_amount"].isna().sum())
report = f"""# Data quality report

Synthetic educational data only. Median imputation is a demonstration assumption;
it must not be used to invent contractual amounts for real billing or lending.

| Check | Result |
| --- | ---: |
| Raw rows | {len(df)} |
| Exact duplicate rows removed | {num_duplicates} |
| Missing amounts before deduplication | {df['loan_amount'].isna().sum()} |
| Unique records with missing amounts | {missing_unique} |
| Median used for imputation | {median_amount:.2f} |
| Clean rows | {len(df_clean)} |
| Missing amounts after cleaning | {df_clean['loan_amount'].isna().sum()} |

Validated unique IDs, dates, credit-score range, positive amounts, allowed terms,
interest-rate range, binary status flags, and defaults restricted to approvals.
SQL consumes this cleaned output and reconciles its totals against Pandas.
"""
Path("reports/data_quality.md").write_text(report)
# --- Step 5: Save the cleaned dataset ---
df_clean.to_csv("auto_loan_data_clean.csv", index=False)
print("\nCleaned dataset saved as auto_loan_data_clean.csv")
