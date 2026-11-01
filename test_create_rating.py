import pytest


STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers=auth,
    )

    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id
    api.delete(f"/api/ratings/{res.json()['id']}", headers=auth)


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": stars},
        headers=auth,
    )

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: decimal, text and missing stars are refused with the API's error message.
@pytest.mark.parametrize(
    "payload, expected_error",
    [
        ({"stars": 3.5}, "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"),
        ({"stars": "3"}, "json: cannot unmarshal string into Go struct field Rating.stars of type int"),
        ({}, STARS_ERROR),
    ],
    ids=["decimal", "text", "missing"],
)
def test_stars_type(api, auth, pizza_id, payload, expected_error):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, **payload},
        headers=auth,
    )

    assert res.status_code == 400
    assert res.json() == {"error": expected_error}


# C3: a pizza id that does not exist is refused.
def test_missing_pizza_is_refused(api, auth):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": 999999999, "stars": 3},
        headers=auth,
    )

    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: a missing or short token is refused.
@pytest.mark.parametrize(
    "headers",
    [None, {"Authorization": "token abc"}],
    ids=["none", "wrong-length"],
)
def test_invalid_token_is_refused(api, pizza_id, headers):
    kwargs = {} if headers is None else {"headers": headers}
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        **kwargs,
    )

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
