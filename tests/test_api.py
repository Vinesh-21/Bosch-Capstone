#test_api.py

import pytest

from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_summary(client:AsyncClient):
    response = await client.get("/health-summary")
    assert response.status_code == 200
    data = response.json()
    assert "KPI_Metrics" in data
    assert "decay_status" in data


@pytest.mark.asyncio
async def test_add_bulk(client: AsyncClient):
    sample_sensors = [
        {
            "lp": 1.0,
            "v": 2.0,
            "GTT": 300.0,
            "GTn": 50.0,
            "GGn": 50.0,
            "Ts": 20.0,
            "Tp": 25.0,
            "T48": 30.0,
            "T1": 50.0,
            "T2": 60.0,
            "P48": 1.0,
            "P1": 2.0,
            "P2": 3.0,
            "Pexh": 0.5,
            "TIC": 1.0,
            "mf": 0.1,
            "decay_comp": 0.1,
            "decay_turbine": 0.2,
            "time": 1233
        }
    ]
    response = await client.post("/add_bulk", json=sample_sensors)
    assert response.status_code == 200

    data = response.json()
    assert "sensor_reading" in data
    
    returned_reading = data["sensor_reading"][0]
    returned_reading.pop("id", None)

    requested_reading = sample_sensors[0]

    assert returned_reading == requested_reading


@pytest.mark.asyncio
async def test_add_KPI(client):
    sample_kpis = [
        {
            "fuel_per_knot": 1.1,
            "fuel_per_torque": 0.9,
            "fuel_per_revolution": 0.5,
            "propeller_imbalance": 0.02,
            "compressor_temp_ratio": 1.05,
            "turbine_temp_ratio": 1.1,
            "compressor_pressure_ratio": 2.0,
            "expansion_ratio": 1.5,
            "torque_per_rpm": 0.8,
            "power_per_knot": 1.2,
            "tic_efficiency": 0.95
        }
    ]
    response = await client.post("/add_KPI", json=sample_kpis)
    assert response.status_code == 200
    data = response.json()
    assert "KPI_Records" in data
    assert len(data["KPI_Records"]) == len(sample_kpis)


@pytest.mark.asyncio
async def test_sensor_metrics_insert_and_fetch(client:AsyncClient):
    sample_sensor = {
        "lp": 1.0,
        "v": 2.0,
        "GTT": 300.0,
        "GTn": 50.0,
        "GGn": 50.0,
        "Ts": 20.0,
        "Tp": 25.0,
        "T48": 30.0,
        "T1": 50.0,
        "T2": 60.0,
        "P48": 1.0,
        "P1": 2.0,
        "P2": 3.0,
        "Pexh": 0.5,
        "TIC": 1.0,
        "mf": 0.1,
        "decay_comp": 0.1,
        "decay_turbine": 0.2,
        "time": 1758634671
    }

    # First insert
    await client.post("/add_bulk", json=[sample_sensor])

    # Then fetch
    response = await client.get("/sensor-metrics/")
    assert response.status_code == 200
    data = response.json()

    for key in sample_sensor:
        assert key in data
        assert data[key] == sample_sensor[key]


@pytest.mark.asyncio
async def test_anomaly_alerts(client:AsyncClient):
    sample_sensor = {
        "lp": 1.0,
        "v": 2.0,
        "GTT": 300.0,
        "GTn": 50.0,
        "GGn": 50.0,
        "Ts": 20.0,
        "Tp": 25.0,
        "T48": 30.0,
        "T1": 50.0,
        "T2": 60.0,
        "P48": 1.0,
        "P1": 2.0,
        "P2": 3.0,
        "Pexh": 0.5,
        "TIC": 1.0,
        "mf": 0.1,
        "decay_comp": 0.1,
        "decay_turbine": 0.2,
        "time": 1758634671
    }

    response = await client.post("/add_bulk", json=[sample_sensor])
    data = response.json()

    sensor_id = (data["sensor_reading"][0])["id"]
    sample_alert = {
        "sensor_id": sensor_id,
        "kpi_name": "fuel_per_knot",
        "kpi_data": 1.23,
        "alert_message": "Performance_Anomaly",
        "severity": "WARNING"
    }

    response_alert = await client.post("/anomaly-alerts", json=sample_alert)
    assert response_alert.status_code == 200
    data = response_alert.json()
    assert data["status"] == "Alert created"
    assert "alert_id" in data
