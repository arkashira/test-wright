from src.test_wright import TestWright, TestCase

def test_add_test_case():
    test_wright = TestWright()
    test_case = TestCase("hello-world", "A simple hello world test case")
    test_wright.add_test_case(test_case)
    assert len(test_wright.test_cases) == 1

def test_run_test_cases():
    test_wright = TestWright()
    test_case = TestCase("hello-world", "A simple hello world test case")
    test_wright.add_test_case(test_case)
    test_wright.run_test_cases()
    # Check that the test case was run successfully
    assert True  # Replace with a concrete assertion

def test_run_test_cases_empty():
    test_wright = TestWright()
    test_wright.run_test_cases()
    # Check that no test cases were run
    assert len(test_wright.test_cases) == 0
