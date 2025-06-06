from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel

from json_context_manager import JsonContextManager
from datetime import datetime

import logic

app = FastAPI()

class Message(BaseModel):
    message: str
    language_from: str
    languages_to: list[str]

def outcome(message, response):
    today = datetime.now().date()
    now = datetime.now().time()
    return {
        "date": str(today),
        "time": str(now),
        "message": message.message,
        "language_from": message.language_from,
        "languages_to": message.languages_to,
        "trans": response,
    }

def find_user(username, filename):
    with JsonContextManager(f"{filename}", "r") as file:
        for i in file.content:
            if i["username"] == username:
                return i
        raise Exception("User not found")

def verify_user(username, password):
    with JsonContextManager("DB/users.json", "r") as users:
        for i in users.content:
            if i["username"] == username and i["password"] == password:
                return True

        return False


@app.post("/translate")
async def post(message: Message, username: str | None = Header(default=None), password: str | None = Header(default=None)):
    with JsonContextManager("DB/users.json", "r+") as users:
        for i in users.content:
            if i["username"] == username and i["password"] == password:
                with JsonContextManager("DB/history.json", "r+") as history:
                    response = logic.translate(message.message, message.languages_to, lang_code_from=message.language_from)
                    outcome_mes = outcome(message, response)
                    for j in history.content:
                        if j["username"] == username:
                            j["history"].append(outcome_mes)

                    return outcome_mes

    raise HTTPException(status_code=401, detail="Unauthorized")

@app.put("/users")
async def create_user(username: str = Header(default=None), password: str = Header(default=None)):
    with JsonContextManager("DB/users.json", "r+") as users:
        for i in users.content:
            if i["username"] == username:
                raise HTTPException(status_code=400, detail="The user already exists")

        users.content.append({
            "username": username,
            "password": password,
        })

    with JsonContextManager("DB/history.json", "r+") as history:
        history.content.append({
            "username": username,
            "history": [],
        })

@app.delete("/users")
async def delete_user(username: str = Header(default=None), password: str = Header(default=None)):
    with JsonContextManager("DB/users.json", "r+") as users:
        for i in users.content:
            if i["username"] == username and i["password"] == password:
                users.content.remove(i)
                with JsonContextManager("DB/history.json", "r+") as history:
                    user = find_user(username, "DB/history.json")
                    history.content.remove(user)
                return

        raise HTTPException(status_code=404, detail="User not found")

@app.get("/history")
async def get_history(username: str = Header(default=None), password: str = Header(default=None), quantity: str = Query(default='1')):
    if not verify_user(username, password):
        raise HTTPException(status_code=404, detail="User not found")

    user = find_user(username, "DB/history.json")

    if 'all' in quantity:
        return user["history"]
    elif type(quantity) == str:
        raise HTTPException(status_code=400, detail="Invalid quantity")
    elif int(quantity) > len(user["history"]):
        raise HTTPException(status_code=400, detail="quantity is too large")
    elif int(quantity) < 0:
        raise HTTPException(status_code=400, detail="quantity must be 0 or greater")
    else:
        slice_start = len(user["history"]) - int(quantity)
        return user["history"][slice_start:]

@app.delete("/history")
async def delete_user_history(username: str = Header(default=None), password: str = Header(default=None)):
    if not verify_user(username, password):
        raise HTTPException(status_code=404, detail="User not found")

    with JsonContextManager("DB/history.json", "r+") as history:
        for i in history.content:
            if i["username"] == username:
                i["history"].clear()