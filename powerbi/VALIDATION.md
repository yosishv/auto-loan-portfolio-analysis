# Validation record

## Automated checks

- Cleaning and SQL report generation completed successfully.
- Five unit tests passed, including every exported credit-band and dealer row.
- Source/model field references and report canvas boundaries passed.
- All 33 schema-bearing project/report files passed Microsoft public JSON schema validation.
  The semantic model BIM was parsed and checked for references, not executed in Analysis Services.
- No tracked data files or SQL outputs changed after regeneration.

## Source fingerprint

Cleaned CSV SHA-256: `b9c7d68f1abc42146a7f42a6eae327a1800b8ca070c95207891d822a49977cfe`

SQL reference commit: `93fa47831d5e03e5fe36e1672c7530bfc65332d1`.
Expected portfolio: 5,000 applications; 3,212 approvals; 473 defaults;
64.24% approval rate; 14.73% default rate among approved loans.

## Still required in Power BI Desktop

- Open the project and resolve any Desktop compatibility issues.
- Set the source path and execute Power Query refresh.
- Execute DAX validation queries and reconcile all segment rows.
- Check slicer interactions, blank division behavior, formatting, and layout.
- Record the Desktop version, actual validation date, active filters, and output.
- Export genuine screenshots and optionally save a PBIX.

No native Power BI execution or screenshot validation has been performed.
