from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "server-health-api"
    assert "timestamp" in data
    print("test_health_check passed")

def test_get_all_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data
    print("test_get_all_metrics passed")

def test_cpu_metrics():
    response = client.get("/metrics/cpu")
    assert response.status_code == 200
    data = response.json()
    assert "usage_percent" in data
    assert "core_count" in data
    assert data["core_count"] > 0
    print("test_cpu_metrics passed")

def test_memory_metrics():
    response = client.get("/metrics/memory")
    assert response.status_code == 200
    data = response.json()
    assert "total_gb" in data
    assert "usage_percent" in data
    assert data["total_gb"] > 0
    print("test_memory_metrics passed")

def test_disk_metrics():
    response = client.get("/metrics/disk")
    assert response.status_code == 200
    data = response.json()
    assert "total_gb" in data
    assert "free_gb" in data
    assert data["total_gb"] > 0
    print("test_disk_metrics passed")

if __name__ == "__main__":
    test_health_check()
    test_get_all_metrics()
    test_cpu_metrics()
    test_memory_metrics()
    test_disk_metrics()
    print("\nAll tests passed.")