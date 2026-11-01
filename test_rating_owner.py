def assert_owner_still_has_rating(api, auth, rating):
    owner_read = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating


def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)

    assert 400 <= res.status_code < 500
    assert_owner_still_has_rating(api, auth, rating)


def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    res = api.put(
        f"/api/ratings/{rating['id']}",
        json={"stars": 5},
        headers=other_auth,
    )

    assert 400 <= res.status_code < 500
    assert_owner_still_has_rating(api, auth, rating)


def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)

    assert 400 <= res.status_code < 500
    assert_owner_still_has_rating(api, auth, rating)
