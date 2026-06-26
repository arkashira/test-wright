# Test Wright

A web dashboard for monitoring code quality.

## Features

* Displays a line chart of test runs per day for the last 30 days
* Shows pass rate percentage with color coding
* Lists flaky tests that failed > 30% of runs in the past week
* Protected by OAuth (GitHub) login

## Requirements

* Python 3.8+
* Poetry

## Installation

1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`
3. Run tests: `poetry run pytest`
