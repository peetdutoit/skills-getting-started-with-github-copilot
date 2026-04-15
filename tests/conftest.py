import copy

from src.app import activities

_original_activities = copy.deepcopy(activities)


def pytest_configure(config):
    # Ensure `src.app.activities` is reset before each test run
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))


def pytest_runtest_setup(item):
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
