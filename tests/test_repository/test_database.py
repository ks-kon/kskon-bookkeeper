from bookkeeper.repository.database import DatabaseConnection

import pytest

@pytest.fixture
def database():
    DatabaseConnection()
