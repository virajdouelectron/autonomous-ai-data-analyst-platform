def test_query_generation(client):
    """Test query generation endpoint."""
    response = client.post(
        "/api/query",
        json={
            "question": "What is the average salary?",
            "column_names": ["name", "age", "salary"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["success", "warning"]
    assert "code" in data
