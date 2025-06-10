import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_zone_and_place_crud(async_client: AsyncClient):
    # Create branch for zones
    resp = await async_client.post("/branches", json={"name": "Branch Z", "address": "Addr Z"})
    branch = resp.json()
    bid = branch["id"]

    # Zones list empty
    resp = await async_client.get(f"/zones?branch_id={bid}&skip=0&limit=10")
    assert resp.status_code == 200
    assert resp.json() == []

    # Create zone
    zone_data = {"branch_id": bid, "name": "Zone 1"}
    resp = await async_client.post("/zones", json=zone_data)
    assert resp.status_code == 201
    zone = resp.json()
    zid = zone["id"]
    assert zone["branch_id"] == bid

    # Get zones
    resp = await async_client.get(f"/zones?branch_id={bid}&skip=0&limit=10")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # Get zone detail
    resp = await async_client.get(f"/zones/{zid}")
    assert resp.status_code == 200

    # Update zone
    resp = await async_client.put(f"/zones/{zid}", json={"name":"Zone 1B"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Zone 1B"

    # Create place
    place_data = {"zone_id": zid, "name": "Seat A"}
    resp = await async_client.post("/places", json=place_data)
    assert resp.status_code == 201
    place = resp.json()
    pid = place["id"]

    # Get places list
    resp = await async_client.get(f"/places?zone_id={zid}&skip=0&limit=10")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # Get place detail
    resp = await async_client.get(f"/places/{pid}")
    assert resp.status_code == 200

    # Update place
    resp = await async_client.put(f"/places/{pid}", json={"name":"Seat B"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Seat B"

    # Delete place
    resp = await async_client.delete(f"/places/{pid}")
    assert resp.status_code == 204

    # Delete zone
    resp = await async_client.delete(f"/zones/{zid}")
    assert resp.status_code == 204
