from test_wright import TestWright, TestResult
import json
import os

def test_trigger_test():
    test_wright = TestWright()
    test_result = test_wright.trigger_test("passing_test")
    assert test_result.test_name == "passing_test"
    assert test_result.result

def test_trigger_failing_test():
    test_wright = TestWright()
    test_result = test_wright.trigger_test("failing_test")
    assert test_result.test_name == "failing_test"
    assert not test_result.result

def test_store_test_results():
    test_wright = TestWright()
    test_wright.trigger_test("passing_test")
    test_wright.trigger_test("failing_test")
    test_wright.store_test_results()
    with open("test_results.json", "r") as f:
        test_results = json.load(f)
    assert len(test_results) == 2
    assert test_results[0]["test_name"] == "passing_test"
    assert test_results[0]["result"]
    assert test_results[1]["test_name"] == "failing_test"
    assert not test_results[1]["result"]
    os.remove("test_results.json")

def test_get_integration_docs():
    test_wright = TestWright()
    integration_docs = test_wright.get_integration_docs()
    assert integration_docs == "Integration documentation for common CI/CD systems"
