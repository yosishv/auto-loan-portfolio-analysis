# Power BI metric definitions

Import `auto_loan_data_clean.csv` as a table named `loans`. These are proposed
measures for rebuilding or refreshing the report; they have not been executed
in Power BI here. Format rate measures as percentages without multiplying by 100.

```dax
Applications = COUNTROWS(loans)
Approved Loans = SUM(loans[approved])
Defaults = SUM(loans[defaulted])
Approval Rate = DIVIDE([Approved Loans], [Applications])
Default Rate = DIVIDE([Defaults], [Approved Loans])
Average Offered Interest Rate = AVERAGE(loans[interest_rate])
```

Calculated column:

```dax
Credit Band = SWITCH(TRUE(),
    loans[credit_score] < 580, "300-579",
    loans[credit_score] < 640, "580-639",
    loans[credit_score] < 700, "640-699",
    loans[credit_score] < 760, "700-759",
    "760-850")
```

With no filters, verify 5,000 applications, 3,212 approvals and 473 defaults.
Compare each credit-band and dealer visual to the exported CSV reports. Check
zero-approval selections display blank rather than division errors. Save the
PBIX and refreshed screenshots only after these checks pass. Historical README
screenshots do not establish parity with the current SQL outputs.
