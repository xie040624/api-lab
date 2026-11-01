import pytest


def test_create_rating(api, auth, pizza_id):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers=auth,
    )

    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id
    api.delete(f"/api/ratings/{res.json()['id']}", headers=auth)


@pytest.mark.parametrize(
    "payload, expected_error",
    [
        ({"stars": 0}, "number of stars must be between 1 and 5 (inclusive)"),
        ({"stars": 6}, "number of stars must be between 1 and 5 (inclusive)"),
        ({"stars": 3.5}, "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"),
        ({"stars": "3"}, "json: cannot unmarshal string into Go struct field Rating.stars of type int"),
        ({}, "number of stars must be between 1 and 5 (inclusive)"),
    ],
    ids=["below-range", "above-range", "decimal", "string", "missing"],
)
def test_create_rating_invalid_stars(api, auth, pizza_id, payload, expected_error):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, **payload},
        headers=auth,
    )

    assert res.status_code == 400
    assert res.json() == {"error": expected_error}


def test_create_rating_with_missing_pizza(api, auth):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": 999999999, "stars": 3},
        headers=auth,
    )

    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


@pytest.mark.parametrize(
    "headers",
    [None, {"Authorization": "auth"}, {"Authorization": "token abc"}],
    ids=["missing", "malformed", "short"],
)
def test_create_rating_with_invalid_token(api, pizza_id, headers):
    kwargs = {} if headers is None else {"headers": headers}
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        **kwargs,
    )

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
