"""Source/model checks and independent SQL parity, not a Power BI runtime test."""
import json
from pathlib import Path
import sqlite3
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'powerbi'


class PowerBIProjectTest(unittest.TestCase):
    def test_project_references_and_visual_fields(self):
        project = json.loads((PROJECT / 'AutoLoan.pbip').read_text())
        report = PROJECT / project['artifacts'][0]['report']['path']
        definition = json.loads((report / 'definition.pbir').read_text())
        model_dir = report / definition['datasetReference']['byPath']['path']
        model = json.loads((model_dir / 'model.bim').read_text())['model']
        table = model['tables'][0]
        available = {kind: {v['name'] for v in table[key]} for kind, key in
                     [('Measure', 'measures'), ('Column', 'columns')]}
        self.assertEqual(len(available['Measure']), 6)
        pages = json.loads((report / 'definition/pages/pages.json').read_text())
        self.assertEqual(len(pages['pageOrder']), 3)
        for name in pages['pageOrder']:
            page_dir = report / 'definition/pages' / name
            page = json.loads((page_dir / 'page.json').read_text())
            visuals = list(page_dir.glob('visuals/*/visual.json'))
            self.assertTrue(visuals)
            for path in visuals:
                visual = json.loads(path.read_text())
                pos = visual['position']
                self.assertGreaterEqual(pos['x'], 0)
                self.assertGreaterEqual(pos['y'], 0)
                self.assertLessEqual(pos['x'] + pos['width'], page['width'])
                self.assertLessEqual(pos['y'] + pos['height'], page['height'])
                for role in visual['visual'].get('query', {}).get('queryState', {}).values():
                    for projection in role['projections']:
                        kind, field = next(iter(projection['field'].items()))
                        self.assertEqual(field['Expression']['SourceRef']['Entity'], 'loans')
                        self.assertIn(field['Property'], available[kind])

    def test_source_counts_and_every_exported_segment(self):
        clean = pd.read_csv(ROOT / 'auto_loan_data_clean.csv')
        self.assertTrue(clean.loan_id.is_unique)
        self.assertEqual((len(clean), int(clean.approved.sum()), int(clean.defaulted.sum())),
                         (5000, 3212, 473))
        self.assertFalse(((clean.defaulted == 1) & (clean.approved == 0)).any())
        # Interval cut independently verifies the DAX/SQL SWITCH boundaries.
        clean['credit_band'] = pd.cut(clean.credit_score,
            [300, 580, 640, 700, 760, 851], right=False,
            labels=['300-579', '580-639', '640-699', '700-759', '760-850']).astype(str)
        bands = pd.read_csv(ROOT / 'reports/credit_bands.csv').set_index('credit_band')
        defaults = pd.read_csv(ROOT / 'reports/defaults_by_credit_band.csv').set_index('credit_band')
        for band, group in clean.groupby('credit_band'):
            with self.subTest(band=band):
                self.assertEqual(len(group), int(bands.loc[band, 'num_loans']))
                self.assertAlmostEqual(round(group.approved.mean() * 100, 1), bands.loc[band, 'approval_rate_pct'])
                self.assertAlmostEqual(round(group.interest_rate.mean(), 2), bands.loc[band, 'avg_interest_rate'])
                expected = defaults.loc[band]
                self.assertEqual((len(group), int(group.approved.sum()), int(group.defaulted.sum())),
                    (int(expected.applications), int(expected.approved_loans), int(expected.defaults)))
                self.assertAlmostEqual(group.defaulted.sum() / group.approved.sum() * 100, expected.default_rate_pct)
        dealers = pd.read_csv(ROOT / 'reports/dealers.csv').set_index('dealer_id')
        self.assertEqual(set(dealers.index), set(clean.dealer_id))
        for dealer, group in clean.groupby('dealer_id'):
            with self.subTest(dealer=dealer):
                expected = dealers.loc[dealer]
                self.assertEqual(len(group), int(expected.total_loans))
                self.assertEqual(int(group.approved.sum()), int(expected.approved_loans))
                self.assertAlmostEqual(round(group.defaulted.sum() / group.approved.sum() * 100, 1), expected.default_rate_pct)
        with sqlite3.connect(ROOT / 'auto_loans.db') as conn:
            totals = conn.execute('SELECT COUNT(*), SUM(approved), SUM(defaulted) FROM loans').fetchone()
        self.assertEqual(totals, (5000, 3212, 473))


if __name__ == '__main__':
    unittest.main()
