import pytest

from config import TEST_DATABASE_URI


@pytest.fixture(scope="session", autouse=True)
def mock_sqlalchemy_session(monkeypatch):
    monkeypatch.setenv("DATABASE_URI", TEST_DATABASE_URI)
