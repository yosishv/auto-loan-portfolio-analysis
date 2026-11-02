# Data quality report

Synthetic educational data only. Median imputation is a demonstration assumption;
it must not be used to invent contractual amounts for real billing or lending.

| Check | Result |
| --- | ---: |
| Raw rows | 5015 |
| Exact duplicate rows removed | 15 |
| Missing amounts before deduplication | 101 |
| Unique records with missing amounts | 100 |
| Median used for imputation | 26200.00 |
| Clean rows | 5000 |
| Missing amounts after cleaning | 0 |

Validated unique IDs, dates, credit-score range, positive amounts, allowed terms,
interest-rate range, binary status flags, and defaults restricted to approvals.
SQL consumes this cleaned output and reconciles its totals against Pandas.
