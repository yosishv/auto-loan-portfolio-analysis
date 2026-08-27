# Auto Loan Portfolio Analysis

An end-to-end data analytics project analyzing auto-loan approval patterns, interest rates, credit risk, defaults, and dealer-level performance.

The project uses Python and Pandas for data generation and preparation, SQLite and SQL for analysis, and Power BI for visualization.

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
- Inconsistent values
- Formatting issues

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
```

The SQLite database is saved as:

```text
auto_loans.db
```

## Key Findings

### Credit-score and approval patterns

Loan approval rates varied substantially across the five credit-score bands, ranging from approximately 17.7% to 91.1%.

Higher-credit-score groups generally experienced:

- Higher approval rates
- Lower average interest rates
- Lower default rates

Average interest rates ranged from approximately 11.5% in the highest-risk band to 5.6% in the lowest-risk band.

### Default risk by credit-score band

Among approved loans, default rates varied from approximately 9.6% to 20.5%.

This represents nearly a twofold difference between the lowest- and highest-risk credit-score groups.

### Dealer-level risk

The analysis ranked 15 dealer partners by default rate.

The highest-risk dealer had a default rate of approximately 19.6%, compared with approximately 10.9% for the lowest-risk dealer.

This difference suggests that dealer-level monitoring may provide additional insight beyond applicant-level credit metrics.

## Power BI Dashboard

The Power BI dashboard presents interactive views of:

- Total loan applications
- Approval rate
- Default rate
- Average interest rate
- Credit-score segmentation
- Default rates by credit-score band
- Dealer-level default performance

During dashboard validation, a calculation issue affecting the default-rate metric was identified and corrected.

dashboard screenshot here:
<img width="1056" height="780" alt="2-re" src="https://github.com/user-attachments/assets/1a006eed-d071-498a-9e84-f57583aaac66" />
<img width="1067" height="822" alt="4-re" src="https://github.com/user-attachments/assets/7a192634-aa23-4276-b6e7-6af151d62d82" />
<img width="1047" height="822" alt="3-re" src="https://github.com/user-attachments/assets/02408d72-d1eb-400c-b0a9-867eefd28eae" />



```text

```

## Repository Structure

```text
auto-loan-portfolio-analysis/
│
├── 01_generate_data.py
├── 02_sql_analysis.py
├── 03_clean_data.py
├── auto_loan_data.csv
├── auto_loan_data_clean.csv
├── auto_loans.db
└── README.md
```

## How to Run the Project

Clone the repository:

```bash
git clone https://github.com/yosishv/auto-loan-portfolio-analysis.git
cd auto-loan-portfolio-analysis
```

Install the required Python packages:

```bash
pip install pandas
```

Run the scripts in this order:

```bash
python 01_generate_data.py
python 03_clean_data.py
python 02_sql_analysis.py
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
- The dashboard file is not included unless separately added to the repository.

## Author

**Yosish Varma Datla**

MSIS Candidate | Data and Business Analytics | SQL | Python | Power BI

- GitHub: [yosishv](https://github.com/yosishv)
- LinkedIn: [yosish-v-625647a1](https://linkedin.com/in/yosish-v-625647a1)
