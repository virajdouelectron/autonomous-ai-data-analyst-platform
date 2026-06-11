def test_insights_generation(client):
    """Test insights generation endpoint."""
    response = client.post(
        "/api/insights",
        json={
            "data_summary": "Dataset with 4 rows",
            "prompt": "What are the key insights?"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["success", "warning"]
    assert "insights" in data
