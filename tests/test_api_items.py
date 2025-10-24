def test_crud_happy_path(client):
    # Create
    r = client.post("/items", json={"name": "Pen", "price": 2.0, "description": "Pen"})
    assert r.status_code == 201
    body = r.json()
    item_id = body["id"]  # Get the generated ID
    assert body["name"] == "Pen"
    assert body["price"] == 2.0
    assert "created_at" in body
    assert "updated_at" in body

    # List
    r = client.get("/items")
    assert r.status_code == 200
    items = r.json()
    assert any(i["id"] == item_id for i in items)

    # Get
    r = client.get(f"/items/{item_id}")
    assert r.status_code == 200
    item = r.json()
    assert item["name"] == "Pen"

    # Update (using PATCH for partial update)
    r = client.patch(
        f"/items/{item_id}", json={"name": "Blue Pen", "price": 2.5}
    )
    assert r.status_code == 200
    item = r.json()
    assert item["name"] == "Blue Pen"
    assert item["price"] == 2.5

    # Delete
    r = client.delete(f"/items/{item_id}")
    assert r.status_code == 204

    # Get after delete -> 404
    r = client.get(f"/items/{item_id}")
    assert r.status_code == 404


def test_api_validation_and_errors(client):
    # 400 on invalid body
    r = client.post("/items", json={"name": "X", "price": 1.0})
    assert r.status_code == 422  # pydantic catches min_length

    r = client.post("/items", json={"name": "", "price": 1.0})
    assert r.status_code == 422

    r = client.post("/items", json={"name": "X", "price": -1})
    assert r.status_code == 422

    # 404 on not found
    r = client.get("/items/999")
    assert r.status_code == 404

    # 404 on update/delete not found
    r = client.patch("/items/999", json={"name": "A", "price": 1.0})
    assert r.status_code == 404

    r = client.delete("/items/999")
    assert r.status_code == 404


def test_partial_updates(client):
    # Create an item
    r = client.post("/items", json={"name": "Original", "price": 10.0, "description": "Original desc"})
    assert r.status_code == 201
    item_id = r.json()["id"]
    
    # Update only the price
    r = client.patch(f"/items/{item_id}", json={"price": 15.0})
    assert r.status_code == 200
    item = r.json()
    assert item["name"] == "Original"  # Should remain unchanged
    assert item["description"] == "Original desc"  # Should remain unchanged
    assert item["price"] == 15.0  # Should be updated
    
    # Update only the name
    r = client.patch(f"/items/{item_id}", json={"name": "Updated Name"})
    assert r.status_code == 200
    item = r.json()
    assert item["name"] == "Updated Name"  # Should be updated
    assert item["description"] == "Original desc"  # Should remain unchanged
    assert item["price"] == 15.0  # Should remain from previous update
    
    # Verify timestamps are different (updated_at should be newer than created_at)
    assert item["created_at"] != item["updated_at"]
