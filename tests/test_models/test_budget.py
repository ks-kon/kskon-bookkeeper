from datetime import datetime

import pytest

# from bookkeeper.bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.database import DatabaseConnection
from bookkeeper.models.budget import Budget


@pytest.fixture
def db():
    return DatabaseConnection()

def test_init_budget():
    b = Budget(DatabaseConnection(), 1000, 5000, 100000)
    assert b.week_budget == 5000

