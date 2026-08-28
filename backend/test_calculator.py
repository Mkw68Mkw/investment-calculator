import unittest

from calculator import (
    build_monthly_history,
    calculate_future_value,
    monthly_rate,
    next_month_value,
    yearly_history,
)


class MonthlyRateTests(unittest.TestCase):
    def test_zero_annual_rate_gives_zero_monthly_rate(self):
        self.assertEqual(monthly_rate(0.0), 0.0)

    def test_annual_rate_compounds_to_itself_over_twelve_months(self):
        rm = monthly_rate(0.08)
        self.assertAlmostEqual((1 + rm) ** 12 - 1, 0.08)


class MonthlyHistoryTests(unittest.TestCase):
    def test_month_zero_equals_starting_capital(self):
        history = build_monthly_history(rj=0.08, SK=40000, EM=1000, n=40)
        self.assertEqual(history[0]["month"], 0)
        self.assertEqual(history[0]["invested"], 40000)
        self.assertEqual(history[0]["value"], 40000)

    def test_history_contains_correct_number_of_months(self):
        history = build_monthly_history(rj=0.08, SK=40000, EM=1000, n=40)
        self.assertEqual(len(history), 12 * 40 + 1)
        self.assertEqual(history[-1]["month"], 12 * 40)

    def test_invested_increases_by_contribution_each_month(self):
        SK, EM = 40000, 1000
        history = build_monthly_history(rj=0.08, SK=SK, EM=EM, n=3)
        for entry in history:
            self.assertEqual(entry["invested"], SK + EM * entry["month"])

    def test_value_grows_by_recurrence(self):
        rj, SK, EM = 0.08, 40000, 1000
        rm = monthly_rate(rj)
        history = build_monthly_history(rj=rj, SK=SK, EM=EM, n=2)
        for prev, curr in zip(history, history[1:]):
            self.assertAlmostEqual(
                curr["value"], next_month_value(prev["value"], rm, EM)
            )


class ZeroInputTests(unittest.TestCase):
    def test_zero_monthly_contribution_only_compounds_principal(self):
        rj, SK = 0.08, 40000
        rm = monthly_rate(rj)
        history = build_monthly_history(rj=rj, SK=SK, EM=0, n=5)
        for entry in history:
            self.assertEqual(entry["invested"], SK)
            self.assertAlmostEqual(
                entry["value"], SK * (1 + rm) ** entry["month"]
            )

    def test_zero_return_rate_value_equals_invested(self):
        SK, EM = 40000, 1000
        history = build_monthly_history(rj=0.0, SK=SK, EM=EM, n=10)
        for entry in history:
            self.assertAlmostEqual(entry["value"], entry["invested"])
            self.assertAlmostEqual(entry["value"], SK + EM * entry["month"])


class YearlyHistoryTests(unittest.TestCase):
    def test_yearly_history_selects_every_twelfth_month(self):
        history = build_monthly_history(rj=0.08, SK=40000, EM=1000, n=4)
        yearly = yearly_history(history)
        self.assertEqual([entry["month"] for entry in yearly], [0, 12, 24, 36, 48])

    def test_yearly_entries_match_monthly_entries(self):
        history = build_monthly_history(rj=0.05, SK=10000, EM=250, n=3)
        yearly = yearly_history(history)
        for entry in yearly:
            self.assertEqual(entry, history[entry["month"]])


class FinalValueTests(unittest.TestCase):
    def test_final_value_equals_last_history_entry(self):
        rj, SK, EM, n = 0.08, 40000, 1000, 40
        result = calculate_future_value(rj, SK, EM, n)
        history = build_monthly_history(rj=rj, SK=SK, EM=EM, n=n)
        self.assertEqual(result["total_future_value"], history[-1]["value"])

    def test_components_sum_to_total(self):
        result = calculate_future_value(0.08, 40000, 1000, 40)
        self.assertAlmostEqual(
            result["future_value_start"] + result["future_value_payments"],
            result["total_future_value"],
        )

    def test_matches_original_closed_form(self):
        rj, SK, EM, n = 0.08, 40000, 1000, 40
        rm = monthly_rate(rj)
        expected_start = SK * (1 + rm) ** (12 * n)
        expected_payments = EM * (((1 + rm) ** (12 * n) - 1) / rm)
        result = calculate_future_value(rj, SK, EM, n)
        self.assertAlmostEqual(result["future_value_start"], expected_start, places=4)
        self.assertAlmostEqual(
            result["total_future_value"], expected_start + expected_payments, places=4
        )

    def test_zero_return_closed_form(self):
        SK, EM, n = 40000, 1000, 40
        result = calculate_future_value(0.0, SK, EM, n)
        self.assertAlmostEqual(result["future_value_start"], SK)
        self.assertAlmostEqual(result["future_value_payments"], EM * 12 * n)
        self.assertAlmostEqual(result["total_future_value"], SK + EM * 12 * n)


if __name__ == "__main__":
    unittest.main()
