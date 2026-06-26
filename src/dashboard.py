import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class TestResult:
    date: str
    passed: int
    failed: int

class Dashboard:
    def __init__(self, test_results):
        self.test_results = test_results

    def get_test_runs_per_day(self):
        test_runs = defaultdict(int)
        for result in self.test_results:
            test_runs[result.date] += result.passed + result.failed
        return test_runs

    def get_pass_rate(self):
        total_passed = sum(result.passed for result in self.test_results)
        total_runs = sum(result.passed + result.failed for result in self.test_results)
        return (total_passed / total_runs) * 100 if total_runs > 0 else 0

    def get_flaky_tests(self):
        flaky_tests = []
        for result in self.test_results:
            if result.failed > 0 and (result.failed / (result.passed + result.failed)) > 0.3:
                flaky_tests.append(result)
        return flaky_tests

    def get_color_code(self, pass_rate):
        if pass_rate >= 95:
            return "green"
        elif pass_rate >= 80:
            return "yellow"
        else:
            return "red"

    def get_line_chart_data(self):
        test_runs = self.get_test_runs_per_day()
        dates = sorted(test_runs.keys())
        data = []
        for date in dates:
            data.append({"date": date, "test_runs": test_runs[date]})
        return data

    def get_dashboard_data(self):
        test_runs_per_day = self.get_line_chart_data()
        pass_rate = self.get_pass_rate()
        color_code = self.get_color_code(pass_rate)
        flaky_tests = self.get_flaky_tests()
        return {
            "test_runs_per_day": test_runs_per_day,
            "pass_rate": pass_rate,
            "color_code": color_code,
            "flaky_tests": flaky_tests,
        }
