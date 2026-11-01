import sqlite3
import pandas as pd

# Load the CSV we created earlier into a pandas DataFrame
df = pd.read_csv("auto_loan_data_clean.csv")

# Create (or connect to) a SQL database file called auto_loans.db
conn = sqlite3.connect("auto_loans.db")

# Write our table into that database, calling the table "loans"
df.to_sql("loans", conn, if_exists="replace", index=False)

print("Data loaded into SQL database successfully.")

# Now let's run our FIRST real SQL query.
# This asks: "how many loan applications are in the table, total?"
query = "SELECT COUNT(*) AS total_loans FROM loans"
result = pd.read_sql(query, conn)
print("\nTotal number of loan records:")
print(result)
query2 = """
SELECT
    CASE
        WHEN credit_score < 580 THEN '300-579'
        WHEN credit_score < 640 THEN '580-639'
        WHEN credit_score < 700 THEN '640-699'
        WHEN credit_score < 760 THEN '700-759'
        ELSE '760-850'
    END AS credit_band,
    COUNT(*) AS num_loans,
    ROUND(AVG(approved) * 100, 1) AS approval_rate_pct,
    ROUND(AVG(interest_rate), 2) AS avg_interest_rate
FROM loans
GROUP BY credit_band
ORDER BY credit_band
"""
result2 = pd.read_sql(query2, conn)
print("\nLoan performance by credit score band:")
print(result2)
query3 = """
SELECT
    dealer_id,
    COUNT(*) AS total_loans,
    SUM(approved) AS approved_loans,
    ROUND(AVG(CASE WHEN approved = 1 THEN defaulted END) * 100, 1) AS default_rate_pct
FROM loans
GROUP BY dealer_id
ORDER BY default_rate_pct DESC
"""
result3 = pd.read_sql(query3, conn)
print("\nDealer performance, sorted by default rate (worst first):")
print(result3)
query4 = """
SELECT CASE WHEN credit_score < 580 THEN '300-579'
 WHEN credit_score < 640 THEN '580-639'
 WHEN credit_score < 700 THEN '640-699'
 WHEN credit_score < 760 THEN '700-759' ELSE '760-850' END AS credit_band,
 COUNT(*) AS applications, SUM(approved) AS approved_loans,
 SUM(defaulted) AS defaults,
 100.0 * SUM(defaulted) / NULLIF(SUM(approved), 0) AS default_rate_pct
FROM loans GROUP BY credit_band ORDER BY credit_band
"""
result4 = pd.read_sql(query4, conn)
print(result4)
from pathlib import Path
Path("reports").mkdir(exist_ok=True)
result2.to_csv("reports/credit_bands.csv", index=False)
result3.to_csv("reports/dealers.csv", index=False)
result4.to_csv("reports/defaults_by_credit_band.csv", index=False)
# Independently reconcile SQL totals with the cleaned input.
assert result.iloc[0]["total_loans"] == len(df)
assert result4["applications"].sum() == len(df)
assert result4["approved_loans"].sum() == df["approved"].sum()
assert result4["defaults"].sum() == df["defaulted"].sum()
conn.close()
