import pytest
from io import BytesIO

def test_upload_csv_success(client, sample_csv_content):
    """Test successful CSV upload."""
    file_data = BytesIO(sample_csv_content.encode())
    response = client.post(
        "/api/upload",
        files={"file": ("test.csv", file_data, "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["rows"] == 4
    assert data["columns"] == 4
    assert "name" in data["column_names"]

def test_upload_non_csv_file(client):
    """Test upload of non-CSV file."""
    file_data = BytesIO(b"test content")
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", file_data, "text/plain")}
    )
    
    assert response.status_code == 400
    assert "CSV" in response.json()["detail"]

def test_upload_malformed_csv(client):
    """Test upload of malformed CSV."""
    bad_csv = b"incomplete,csv,row"
    file_data = BytesIO(bad_csv)
    response = client.post(
        "/api/upload",
        files={"file": ("bad.csv", file_data, "text/csv")}
    )
    
    assert response.status_code in [200, 400]
