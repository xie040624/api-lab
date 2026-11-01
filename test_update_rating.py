import pytest


@pytest.mark.parametrize("stars, expected_status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_rating_star_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)

    assert res.status_code == expected_status
    current = api.get(path, headers=auth)
    assert current.status_code == 200
    assert current.json()["stars"] == (stars if expected_status == 200 else 3)
