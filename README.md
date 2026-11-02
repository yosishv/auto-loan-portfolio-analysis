# Auto Loan Portfolio Analysis

A portfolio project using synthetic auto-loan applications to practice data cleaning, SQL reporting, and metric reconciliation.

Python and Pandas prepare the data; SQLite produces reproducible reports. Historical Power BI screenshots are included, with refresh instructions provided separately.

## Project Objectives

This project addresses the following business questions:

- How do credit-score bands affect loan approval rates?
- How do credit scores relate to average interest rates?
- Which credit-score bands have the highest default rates?
- Which dealer partners show the highest default risk?
- What data-quality issues must be addressed before reporting?
- How can portfolio metrics support lending and risk-management decisions?

## Tools and Technologies

- Python
- Pandas
- SQLite
- SQL
- Power BI
- Git and GitHub

## Dataset

The project uses a synthetic dataset containing 5,000 auto-loan records.

The dataset includes fields related to:

- Loan applications
- Approval status
- Credit scores
- Interest rates
- Loan amounts
- Default status
- Dealer partners
- Applicant and loan characteristics

The data is synthetic and is intended for demonstration and educational purposes only. It does not represent real customers or financial institutions.

## Project Workflow

### 1. Generate the data

The `01_generate_data.py` script creates the synthetic auto-loan dataset.

```bash
python 01_generate_data.py
```

### 2. Clean and prepare the data

The `03_clean_data.py` script checks for data-quality issues, including:

- Duplicate records
- Missing values
- Unique IDs, valid dates and numeric ranges
- Allowed terms and consistent approval/default flags

```bash
python 03_clean_data.py
```

The cleaned dataset is saved as:

```text
auto_loan_data_clean.csv
```

### 3. Analyze the data with SQL

The `02_sql_analysis.py` script loads the data into SQLite and performs SQL-based analysis.

```bash
python 02_sql_analysis.py
python -m unittest discover -s tests -v
```

The SQLite database is saved as:

```text
auto_loans.db
```

## Verified findings

The cleaned dataset has 5,000 unique applications. SQL reports are exported to
`reports/credit_bands.csv`, `reports/defaults_by_credit_band.csv`, and `reports/dealers.csv`.

- Approval rates range from 17.7% to 91.1% by credit band.
- Mean offered interest rates (all applications) range from 11.54% to 5.63%.
- Defaults among approved loans range from 21.95% to 9.49% by credit band.
- Dealer default rates range from 19.7% to 10.9% (rounded to one decimal).
- Portfolio default rate is 473 / 3,212 = 14.73%.

The highest credit-band default rate is about 1.49 times the portfolio rate;
this does not support a claim of 2–3 times the portfolio average.
These patterns are intentionally influenced by the synthetic generator's credit,
term, rate and dealer rules. They are demonstrations, not real-world lending findings.
Small approved samples, including 41 approvals in the lowest band, limit comparisons.

## Data quality and metric definitions

See [the generated quality report](reports/data_quality.md). Exact duplicates are
removed; missing loan amounts are median-imputed for this educational exercise.
Real financial reconciliation should flag missing contractual amounts for review,
not substitute estimates. Other validation failures stop the pipeline.

Credit bands are 300–579, 580–639, 640–699, 700–759 and 760–850, inclusive.
Approval rate = approvals / applications. Default rate = defaults / approvals.
Average interest rate describes all application offers, including declined applications.
No observation window or loan seasoning is modeled; default is a simulated outcome.

## Power BI Dashboard

The historical Power BI screenshots illustrate:

- Total loan applications
- Approval rate
- Default rate
- Average interest rate
- Credit-score segmentation
- Default rates by credit-score band
- Dealer-level default performance

The screenshots below are historical. They have not been revalidated against the corrected pipeline. The PBIX file is not included. Use the exported SQL reports as the current numerical reference and refresh Power BI before using screenshots as evidence.

See [Power BI measure definitions](POWER_BI.md) for proposed measures and reconciliation steps.

### Historical screenshots
<img width="1056" height="780" alt="2-re" src="https://github.com/user-attachments/assets/1a006eed-d071-498a-9e84-f57583aaac66" />
<img width="1067" height="822" alt="4-re" src="https://github.com/user-attachments/assets/7a192634-aa23-4276-b6e7-6af151d62d82" />
<img width="1047" height="822" alt="3-re" src="https://github.com/user-attachments/assets/02408d72-d1eb-400c-b0a9-867eefd28eae" />




## Repository files

| File or folder | Purpose |
| --- | --- |
| `01_generate_data.py` | Generate synthetic applications and intentional data defects |
| `03_clean_data.py` | Remove duplicates, impute missing amounts, validate records |
| `02_sql_analysis.py` | Analyze cleaned input and export reconciled SQL reports |
| `auto_loan_data.csv` | Raw demonstration input |
| `auto_loan_data_clean.csv` | Cleaned demonstration input |
| `reports/` | Data-quality report and segment metrics |
| `tests/` | Reconciliation and credit-band boundary checks |
| `POWER_BI.md` | Proposed measures and dashboard verification steps |
| `requirements.txt` | Python dependencies |

`auto_loans.db` is generated locally and excluded from version control.

## How to Run the Project

Run commands from the repository root using Python 3.10 or newer.

Clone the repository:

```bash
git clone https://github.com/yosishv/auto-loan-portfolio-analysis.git
cd auto-loan-portfolio-analysis
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the scripts in this order:

```bash
python 01_generate_data.py
python 03_clean_data.py
python 02_sql_analysis.py
python -m unittest discover -s tests -v
```

## Business Applications

The analysis could support:

- Credit-risk segmentation
- Loan approval policy evaluation
- Interest-rate analysis
- Dealer performance monitoring
- Portfolio-risk reporting
- Data-quality improvement
- Management dashboard development

## Limitations

- The dataset is synthetic.
- Results should not be used for real lending decisions.
- The analysis does not include production-level credit underwriting variables.
- Observed relationships do not necessarily indicate causation.
- The Power BI source file is not included; screenshot values have not been revalidated after the pipeline corrections.

## Author

**Yosish Varma Datla**

MSIS Candidate | Data and Business Analytics | SQL | Python | Power BI

- GitHub: [yosishv](https://github.com/yosishv)
- LinkedIn: [yosish-v-625647a1](https://linkedin.com/in/yosish-v-625647a1)

