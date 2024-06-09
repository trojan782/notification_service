from fastapi import FastAPI
import crud
from models import User, Notification

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/user")
def create_user(user: User):
    return crud.create_user(user)

@app.get("/users")
def get_users():
    return crud.get_all_users()

@app.get("/user/events/{email}")
def get_events(email: str):
    return crud.get_user_events(email)

@app.post("/notify")
def create_notification(notification: Notification):
    return crud.create_notification(notification)

@app.post("/subcribe/{endpoint}")
def subcribe(endpoint: str):
    return crud.subcribe_to_event(endpoint)
