from datetime import datetime, timedelta
from dashboard import Dashboard, TestResult

def test_get_test_runs_per_day():
    test_results = [
        TestResult("2022-01-01", 10, 0),
        TestResult("2022-01-01", 5, 0),
        TestResult("2022-01-02", 8, 2),
    ]
    dashboard = Dashboard(test_results)
    test_runs_per_day = dashboard.get_test_runs_per_day()
    assert test_runs_per_day["2022-01-01"] == 15
    assert test_runs_per_day["2022-01-02"] == 10

def test_get_pass_rate():
    test_results = [
        TestResult("2022-01-01", 10, 0),
        TestResult("2022-01-02", 8, 2),
    ]
    dashboard = Dashboard(test_results)
    pass_rate = dashboard.get_pass_rate()
    assert pass_rate == 90

def test_get_flaky_tests():
    test_results = [
        TestResult("2022-01-01", 10, 0),
        TestResult("2022-01-02", 8, 2),
        TestResult("2022-01-03", 5, 5),
    ]
    dashboard = Dashboard(test_results)
    flaky_tests = dashboard.get_flaky_tests()
    assert len(flaky_tests) == 1
    assert flaky_tests[0].date == "2022-01-03"

def test_get_color_code():
    dashboard = Dashboard([])
    assert dashboard.get_color_code(95) == "green"
    assert dashboard.get_color_code(85) == "yellow"
    assert dashboard.get_color_code(75) == "red"

def test_get_line_chart_data():
    test_results = [
        TestResult("2022-01-01", 10, 0),
        TestResult("2022-01-02", 8, 2),
    ]
    dashboard = Dashboard(test_results)
    line_chart_data = dashboard.get_line_chart_data()
    assert len(line_chart_data) == 2
    assert line_chart_data[0]["date"] == "2022-01-01"
    assert line_chart_data[0]["test_runs"] == 10
    assert line_chart_data[1]["date"] == "2022-01-02"
    assert line_chart_data[1]["test_runs"] == 10

def test_get_dashboard_data():
    test_results = [
        TestResult("2022-01-01", 10, 0),
        TestResult("2022-01-02", 8, 2),
    ]
    dashboard = Dashboard(test_results)
    dashboard_data = dashboard.get_dashboard_data()
    assert "test_runs_per_day" in dashboard_data
    assert "pass_rate" in dashboard_data
    assert "color_code" in dashboard_data
    assert "flaky_tests" in dashboard_data
