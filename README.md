# api-lab

## Ratings input domain model

| Characteristic | Blocks / example inputs |
|---|---|
| จำนวนดาว | ต่ำกว่า 1: `0` / 1–5: `3` / มากกว่า 5: `6` |
| ชนิดของดาว | จำนวนเต็ม: `3` / ทศนิยม: `3.5` / ข้อความ: `"3"` / ไม่มี field: ไม่มี `stars` |
| Pizza | มีอยู่: `pizza_id` จาก fixture / ไม่มีอยู่: `999999999` |
| Token | token ของ user / ไม่มี header / รูปแบบผิด `auth` / token สั้น `token abc` |

Tests cover the base case and each block in `test_create_rating.py`, update boundaries in `test_update_rating.py`, and cross-user ownership in `test_rating_owner.py`.
