import uuid


def new_user():
    return {
        "username": "lab-" + uuid.uuid4().hex[:12],
        "password": "Pizza-2026",
    }


def test_username_already_taken(api):
    user = new_user()
    assert api.post("/api/users", json=user).status_code == 201

    res = api.post("/api/users", json=user)

    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


def test_login_with_wrong_password(api):
    user = new_user()
    assert api.post("/api/users", json=user).status_code == 201

    res = api.post(
        "/api/users/token/login",
        json={**user, "password": "wrong-password"},
    )

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


def test_empty_username(api):
    res = api.post(
        "/api/users",
        json={"username": "", "password": "Pizza-2026"},
    )

    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
