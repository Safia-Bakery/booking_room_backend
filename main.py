import re
from typing import List
from fastapi import FastAPI
from models import User


app = FastAPI(
    title="Book Meeting"
)


fake_users = [
    {"id": 1, "fullname": "Bakhtiyor Bakhriddinov", "phone": "+998977828474", "email": "uzdev27@gmail.com"},
    {"id": 2, "fullname": "Bekzod Sagdullayev", "phone": "+998975564455", "email": "uzbox21@gmail.com"},
    {"id": 3, "fullname": "Ilkhom Aliev", "phone": "+998971156455", "email": "uzlive11@gmail.com"}
]


@app.get("/user/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user["id"] == user_id]
    # return user_id


@app.get("/users")
def get_users(limit: int, offset: int):
    return fake_users[offset:][:limit]


@app.post("/user/{user_id}")
def change_username(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
    current_user["fullname"] = new_name
    return {"status": 200, "data": current_user}


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False


@app.post("/users")
def add_users(users: List[User]):
    fake_users.extend(users)
    return {"status": 200, "data": fake_users}
