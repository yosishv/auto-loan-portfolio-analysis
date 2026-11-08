# Auto Loan Power BI project

This is a source-controlled rebuild of the missing Power BI report. It contains
three report pages, an import model, six DAX measures, and DAX validation queries.
It is a new implementation, not a recovery of the historical PBIX.

**Status: project authored; Power BI Desktop open, refresh, DAX execution,
visual layout inspection, and screenshot export are pending.** JSON schema and
independent CSV/SQL reconciliation checks do not establish Power BI runtime parity.

## Open and refresh on Windows

1. Download or clone the entire repository. Keep the project folders together.
2. Install a current Microsoft Power BI Desktop release that supports PBIP/PBIR.
   If prompted, enable Power BI project/enhanced report format support in Options.
3. Open `powerbi/AutoLoan.pbip`. The report references the adjacent semantic model.
4. In Transform data > Edit parameters, set `DataFilePath` to the full Windows
   path of the repository's `auto_loan_data_clean.csv`. The placeholder is
   `C:\AutoLoanPortfolio\auto_loan_data_clean.csv`; it must be changed if your
   file is elsewhere. Apply changes and refresh the model.
5. Clear all filters. Confirm 5,000 applications, 3,212 approvals, 473 defaults,
   64.24% approval rate, and 14.73% default rate among approvals.
6. Run `AutoLoan.SemanticModel/DAXQueries/Validation.dax` in DAX query view.
   Compare every credit-band and all 15 dealer rows with `../reports/` using
   the rounding rules in `../POWER_BI.md`. Rates returned by DAX are fractions;
   multiply by 100 only when comparing them with CSV percentage-point columns.
7. Check slicer interactions, zero-approval selections, offered-rate formatting,
   titles, labels, totals, and visual layout. The declined-only query must return
   a blank default rate. Fix any Desktop compatibility or rendering issues.
8. Save the project and optionally use Save As to create a PBIX. Export genuine
   screenshots only after the checks pass. Record the actual Desktop version,
   source-data commit, validation date, filters, and DAX outputs. Remove the
   runtime-pending footer and update documentation only after that evidence exists.

The files contain model and report definitions, not a populated data cache.
No account credentials or Power BI service subscription are embedded or needed
for the local CSV import.

## Report pages

- **Portfolio overview:** six KPI cards, application volume and default-rate
  charts by credit band, and a count/rate reconciliation table.
- **Credit-band analysis:** band slicer, approval and offered-rate charts, and
  detailed counts and rates. Offered interest rates include declined applications.
- **Dealer performance:** dealer slicer, observed default-rate ranking, and
  application/approval/default counts. Comparisons use approved-loan denominators.

All data is synthetic. There is no observation window or loan seasoning.
Defaults are simulated outcomes, not annualized rates. Small samples limit
comparisons; rankings do not demonstrate causal dealer quality.

## Automated checks

From the repository root, after installing `requirements.txt`:

```bash
python 03_clean_data.py
python 02_sql_analysis.py
python -m unittest discover -s tests -v
```

`tests/test_powerbi_project.py` checks report/model references, page boundaries,
and independent credit-band/dealer calculations against the committed SQL exports.
It does not run Power Query, DAX, or the Power BI rendering engine.

## Format references

- [Microsoft: Power BI project report folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report)
- [Microsoft: semantic model folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)
- [Microsoft public JSON schemas](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report)
