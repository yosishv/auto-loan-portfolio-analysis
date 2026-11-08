# Power BI definitions and reconciliation targets

## Current status

The measures below are proposed definitions for rebuilding or refreshing the
dashboard. They have not been executed in Power BI. No PBIX file is included.

A new [Power BI project](powerbi/README.md) implements these definitions in an
import model and three report pages. Set its `DataFilePath` parameter to the
cleaned CSV before refreshing. Desktop loading, Power Query execution, DAX
execution, rendered layout inspection, and screenshot export remain pending.

Historical README screenshots have not been reconciled to the corrected SQL
pipeline. Current numerical results are documented in the exported SQL reports.

## Data source and model

Import `auto_loan_data_clean.csv` as a table named `loans`.

- Use the cleaned file, not `auto_loan_data.csv`, which contains duplicates.
- Each row represents one application; `loan_id` must be unique.
- Set `approved` and `defaulted` to Whole Number.
- Set `credit_score` to Whole Number and `interest_rate` to Decimal Number.
- Set `application_date` to Date.
- Status flags must be 0 or 1; defaults must be restricted to approved loans.
- Use this application-level table for the measures below. Do not append the
  aggregate SQL exports to it or create joins that duplicate application rows.

In the SQL exports, `num_loans` and `total_loans` count applications, including
declines. Label these fields "Applications" in dashboard visuals.

## Proposed measures

```dax
Applications = COUNTROWS(loans)

Approved Loans = SUM(loans[approved])

Defaults = SUM(loans[defaulted])

Approval Rate = DIVIDE([Approved Loans], [Applications])

Default Rate Among Approved Loans =
    DIVIDE([Defaults], [Approved Loans])

Average Offered Interest Rate =
    DIVIDE(AVERAGE(loans[interest_rate]), 100)
```

Format counts as whole numbers with thousands separators. Format the three
rate measures as percentages with two decimal places.

Approval and default measures return fractions. Do not multiply them by 100
before applying Percentage formatting.

The source `interest_rate` stores percentage points: 8.59 means 8.59%.
The proposed interest-rate measure divides by 100 so Percentage formatting
displays it correctly.

The average offered interest rate covers all applications in the current
filter context, including declines. Do not label it as the average rate of
approved or funded loans.

Default rate means simulated defaults divided by approved loans in the same
filter context. Do not divide defaults by all applications or average
credit-band or dealer default percentages to calculate portfolio default rate.

## Credit bands

Create this calculated column:

```dax
Credit Band =
    SWITCH(
        TRUE(),
        loans[credit_score] < 580, "300-579",
        loans[credit_score] < 640, "580-639",
        loans[credit_score] < 700, "640-699",
        loans[credit_score] < 760, "700-759",
        "760-850"
    )
```

This definition assumes the cleaned input has passed validation and contains
credit scores from 300 through 850 with no missing scores.

The bands are inclusive: 300-579, 580-639, 640-699, 700-759, and 760-850.
Display them in that order.

## Unfiltered portfolio targets

Clear slicers and visual, page, and report filters before checking these totals.

| Metric | Expected value | Definition |
| --- | ---: | --- |
| Applications | 5,000 | Cleaned application rows |
| Approved loans | 3,212 | Sum of approved flags |
| Defaults | 473 | Sum of defaulted flags |
| Approval rate | 64.24% | 3,212 / 5,000 |
| Default rate among approved loans | 14.73% | 473 / 3,212 |

These targets describe the currently committed dataset. If the dataset is
regenerated or changed, rerun SQL and update the targets before validating
Power BI.

## Credit-band targets

Sources: `reports/credit_bands.csv` and
`reports/defaults_by_credit_band.csv`.

| Credit band | Applications | Approved loans | Defaults | Approval rate | Default rate among approvals | Average offered interest rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 300-579 | 231 | 41 | 9 | 17.7% | 21.95% | 11.54% |
| 580-639 | 1,011 | 391 | 73 | 38.7% | 18.67% | 10.06% |
| 640-699 | 1,892 | 1,232 | 213 | 65.1% | 17.29% | 8.59% |
| 700-759 | 1,415 | 1,137 | 139 | 80.4% | 12.23% | 7.18% |
| 760-850 | 451 | 411 | 39 | 91.1% | 9.49% | 5.63% |

Approval rates are shown to one decimal to match `credit_bands.csv`.
Default and offered interest rates are shown to two decimals.
Compare at the export's precision; do not round the underlying DAX measures.

## Dealer targets

Compare every dealer's application count, approved count, and default rate
with `reports/dealers.csv`. Dealer default rates in that export are rounded
to one decimal place.

The highest observed dealer default rate is D007 at 19.7%, with 208 approvals
from 336 applications. The lowest is D002 at 10.9%, with 192 approvals from
298 applications.

Dealer totals must reconcile to 5,000 applications and 3,212 approvals.
Calculate the portfolio default rate from the underlying counts, not the
average of the dealer rates.

## Validation before publishing

1. Confirm the model uses the current cleaned CSV and contains 5,000 unique
   application IDs.
2. Match every unfiltered portfolio target above.
3. Match every credit-band row to both credit-band exports.
4. Match all 15 dealer rows to `reports/dealers.csv`.
5. Confirm credit-band and dealer selections recalculate numerator and
   denominator within the same filter context.
6. Confirm a selection with zero approvals returns a blank default rate.
7. Confirm interest-rate values display as percentages correctly; for example,
   the 640-699 band must show 8.59%, not 859%.
8. Check visual titles, tooltips, totals, filters, and narrative annotations
   against the same definitions.
9. Save the PBIX and export replacement screenshots only after reconciliation
   passes. Record the dataset version, validation date, and any active filters.

Do not describe the Power BI report as validated until these checks have
actually been completed.

## Interpretation limits

The data and default outcomes are synthetic. No observation window or loan
seasoning is modeled, so these are not annualized or vintage default rates.

The highest credit-band default rate is approximately 1.49 times the portfolio
rate, not 2-3 times the portfolio average. The lowest credit band has only
41 approvals, which limits comparisons.

Dealer rankings and credit-band patterns describe this simulated dataset.
They do not establish causation or justify real lending decisions.
