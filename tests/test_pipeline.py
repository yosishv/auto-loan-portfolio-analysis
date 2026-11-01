import sqlite3
import unittest
import pandas as pd

class PipelineTest(unittest.TestCase):
    def test_cleaning_and_sql_reconcile(self):
        raw = pd.read_csv('auto_loan_data.csv')
        clean = pd.read_csv('auto_loan_data_clean.csv')
        self.assertEqual(len(clean), len(raw.drop_duplicates()))
        self.assertTrue(clean.loan_id.is_unique)
        self.assertEqual(int(clean.loan_amount.isna().sum()), 0)
        with sqlite3.connect('auto_loans.db') as conn:
            sql = pd.read_sql('SELECT * FROM loans', conn)
        pd.testing.assert_frame_equal(sql, clean)
        totals = pd.read_csv('reports/defaults_by_credit_band.csv')
        self.assertEqual(totals.defaults.sum(), clean.defaulted.sum())
        self.assertEqual(totals.approved_loans.sum(), clean.approved.sum())

    def test_credit_band_boundaries(self):
        scores = [300, 579, 580, 639, 640, 699, 700, 759, 760, 850]
        expected = ['300-579']*2 + ['580-639']*2 + ['640-699']*2 + ['700-759']*2 + ['760-850']*2
        bands = pd.cut(scores, [300,580,640,700,760,851], right=False, labels=['300-579','580-639','640-699','700-759','760-850'])
        self.assertEqual(list(bands), expected)
        with sqlite3.connect(':memory:') as conn:
            pd.DataFrame({'credit_score': scores}).to_sql('loans', conn, index=False)
            result = pd.read_sql("SELECT CASE WHEN credit_score < 580 THEN '300-579' WHEN credit_score < 640 THEN '580-639' WHEN credit_score < 700 THEN '640-699' WHEN credit_score < 760 THEN '700-759' ELSE '760-850' END AS band FROM loans", conn)
        self.assertEqual(result.band.tolist(), expected)

if __name__ == '__main__':
    unittest.main()
