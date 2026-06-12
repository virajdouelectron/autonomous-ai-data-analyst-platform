import pytest
from starlette.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app=app)

@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing."""
    return """name,age,salary,department
John,28,50000,Engineering
Jane,32,60000,Sales
Bob,45,75000,Management
Alice,26,48000,Engineering"""
