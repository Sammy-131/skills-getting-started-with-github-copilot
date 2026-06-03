from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities as activities_data
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy(activities_data)
    yield
    activities_data.clear()
    activities_data.update(original_activities)
