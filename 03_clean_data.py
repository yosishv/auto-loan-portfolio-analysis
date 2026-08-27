import pandas as pd

# Load the raw messy data
df = pd.read_csv("auto_loan_data.csv")

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
# Instead of deleting rows with missing data (which throws away otherwise-good
# information about that loan), we fill missing loan_amount with the median
# loan amount -- a common, defensible approach when values are missing at random.
median_amount = df_clean["loan_amount"].median()
print(f"\nMedian loan amount (used to fill missing values): {median_amount}")

df_clean["loan_amount"] = df_clean["loan_amount"].fillna(median_amount)

print(f"Missing loan_amount values after cleaning: {df_clean['loan_amount'].isna().sum()}")

# --- Step 5: Save the cleaned dataset ---
df_clean.to_csv("auto_loan_data_clean.csv", index=False)
print("\nCleaned dataset saved as auto_loan_data_clean.csv")