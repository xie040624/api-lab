# api-lab

## Ratings input domain model

| Characteristic | Blocks and test covering each block |
|---|---|
| C1: stars value | below 1: `0` and above 5: `6` -> `test_stars_out_of_range`; base 1-5: `3` -> `test_base_choice_is_saved` |
| C2: stars type | whole number: `3` -> `test_base_choice_is_saved`; decimal: `3.5`, text: `"3"`, missing: no `stars` -> `test_stars_type` |
| C3: pizza | exists: fixture `pizza_id` -> `test_base_choice_is_saved`; missing: `999999999` -> `test_missing_pizza_is_refused` |
| C4: token | user's own: `auth` -> `test_base_choice_is_saved`; none and wrong length: `test_invalid_token_is_refused` |

The tests use the base choice of 3 whole-number stars, an existing pizza, and the logged-in user's token. Each non-base test changes one characteristic while keeping the other inputs at their base choices.
