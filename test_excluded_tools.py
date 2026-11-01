import pytest

# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize("excluded", [["Knife"], ["Scissors"]])
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


@pytest.mark.parametrize(
    "excluded",
    [[], ["Knife"], ["Knife", "Pizza cutter"]],
    ids=["zero", "one", "two"],
)
def test_excluded_tool_count(api, auth, excluded):
    res = api.post("/api/pizza", json={"excludedTools": excluded}, headers=auth)

    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


@pytest.mark.xfail(
    reason="Defect 1: excluding all tools returns 500 with an empty body instead of 400 with a JSON error",
    strict=True,
)
def test_excluding_all_tools_returns_error(api, auth):
    res = api.post(
        "/api/pizza",
        json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]},
        headers=auth,
    )

    assert res.status_code == 400
    assert res.json() == {"error": "no tools available"}
