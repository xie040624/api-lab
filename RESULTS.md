# API lab results

## Part 0

- Step 0.1, the number of pizza names: 18
- Step 0.2, status 200, Content-Type application/json, and an AWSALB cookie
- Step 0.3, no token: 401; with token: `{"tools":["Knife","Pizza cutter","Scissors"]}`
- Step 0.4, pizza name observed: `A Giant Carbonara`
- Step 0.12, not run because it was optional
- Step 0.16, excluded-tools blocks: 0, 1, 2, and 3 excluded tools

## Defect report

- Title: Excluding all tools returns an internal server error
- Request: `POST /api/pizza` with `{"excludedTools":["Knife","Pizza cutter","Scissors"]}` and a valid user token
- Expected result: status 400 with a JSON error message, as required by the product owner
- Actual result: status 500 with an empty body; confirmed with curl
- Severity: medium; the client receives no actionable validation error and cannot reliably handle the response

## Part A

- Step A1-A2, create-rating input space covered with 9 tests: base choice, stars below/above range, decimal/text/missing stars, missing pizza, and missing/short token
- Step A3, update stars 0 -> 400 and unchanged, 1 -> 200, 5 -> 200, 6 -> 400 and unchanged
- Step A4, other user status codes: read 404, change 400, delete 400; the owner could still read the unchanged rating

## Made-up token check

- `madeup.txt` contained `Authorization: token 0000000000000000`.
- Read-only `GET /api/ratings` returned status 200 and a JSON list of ratings. No data was created or changed.

## Part B: Reflection

1. API tests can find network failures, authentication or routing problems, and mismatches in the real server's status codes and JSON. A unit test with stubs cannot find those integration failures because it does not contact the server. Unit tests are still useful because they are fast, deterministic, and isolate the code being tested.

2. Each test creates a user with a new name so ratings belong only to that test and cannot be changed by another student's test. The public token belongs to everyone and would make ownership and cleanup unreliable. I would use the same pattern for the shop or hotel project: create or use a test account owned by the test run, create only its data, and clean it up when possible.

3. Every request uses one session because QuickPizza is behind a load balancer and the session keeps the AWSALB cookie that selects the server holding the new user. Without the session, create and login can reach different servers and login may fail with 401. I did not run the optional three no-session runs.

4. The block with all three tools excluded revealed the defect. A 500 with an empty body hides the input problem and gives the client no useful error to display or handle, while a 400 JSON error identifies a rejected request. The test remains as a strict xfail so the defect stays visible and the suite fails when the API is fixed, prompting removal of the marker.

5. Base choice needs 9 tests: `1 + 2 + 3 + 1 + 2 = 9` for the four characteristics. All combinations would need `3 * 4 * 2 * 3 = 72` tests.

6. The other user received 404 for read, 400 for change, and 400 for delete. I would generally expect any 4xx response for all three because the important requirement is that the operation is refused. The different 4xx codes are not a defect here because the exercise specifies the 4xx class, not one exact code, and the owner's rating stayed unchanged.

7. The made-up token returned 200 and a JSON ratings list for the read-only request. In this shared lab environment that is an observed behavior, but accepting an arbitrary token for real data would be a security defect in a real system: a stranger could read ratings. I did not use that token to create or change anything.

8. An API test checks HTTP methods, status codes, headers, JSON fields, and authorization precisely. A web-page test can check things an API test cannot, such as rendered layout, browser interactions, accessibility, and the messages visible to a user.

## Full run

- `pytest -v --html=report.html --self-contained-html`: 33 passed, 1 xfailed (34 tests collected; the repository retains the original create-rating test in `test_ratings.py`)
