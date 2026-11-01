def test_other_user_cannot_read_update_or_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"

    read = api.get(path, headers=other_auth)
    update = api.put(path, json={"stars": 5}, headers=other_auth)
    delete = api.delete(path, headers=other_auth)

    assert 400 <= read.status_code < 500
    assert 400 <= update.status_code < 500
    assert 400 <= delete.status_code < 500

    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating
