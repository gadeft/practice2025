"""
Implementation of API
Examples of usage are in the README.md
"""

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

from json_context_manager import JsonContextManager
import logic

app = FastAPI()

'''Structure of body of /translate post request'''
class Message(BaseModel):
    message: str
    language_from: str
    languages_to: list[str]

'''Body of the response on /translate post request'''
def outcome(message, translation):
    today = datetime.now().date()
    now = datetime.now().time()
    return {
        "date": str(today),
        "time": str(now),
        "message": message.message,
        "language_from": message.language_from,
        "languages_to": message.languages_to,
        "trans": translation,
    }

'''Finds the user by username if the file and returns it'''
def get_user(username, filename):
    with JsonContextManager(f"{filename}", "r") as file:
        for i in file:
            if i["username"] == username:
                return i
        raise Exception("User not found")

'''Finds the user by username in the file and returns True if it exists and False if not'''
def find_user(username, filename):
    with JsonContextManager(f"{filename}", "r") as file:
        for i in file:
            if i["username"] == username:
                return True
        return False

'''
Finds the user in file DB/user.json by username and password. 
Returns True if the user is found and False if not
'''
def verify_user(username, password):
    with JsonContextManager("DB/users.json", "r") as users:
        for i in users:
            if i["username"] == username and i["password"] == password:
                return True
        return False


'''
Translates the message in th request.
Gets message as the body of the request. Gets username and password in the header.
Returns translation and saves it in the history
Raises "401 Unauthorized" if the username or password is incorrect
'''
@app.post("/translate")
async def post(message: Message, username: str | None = Header(default=None), password: str | None = Header(default=None)):
    if not verify_user(username, password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    response = logic.translate(message.message, message.languages_to, message.language_from)
    outcome_mes = outcome(message, response)

    with JsonContextManager("DB/history.json", "r+") as history:
        user = get_user(username, "DB/history.json")
        index = history.index(user)
        user["history"].append(outcome_mes)
        history[index] = user

    return outcome_mes

'''
Creates a new user.
Gets username and password in the header of HTTP request.
Returns nothing.
Raises "409 Conflict" if the user already exists.
'''
@app.put("/users")
async def create_user(username: str = Header(default=None), password: str = Header(default=None)):
    if find_user(username, "DB/users.json"):
        raise HTTPException(status_code=409, detail="User already exists")

    with JsonContextManager("DB/users.json", "r+") as users:
        users.append({
            "username": username,
            "password": password,
        })
    with JsonContextManager("DB/history.json", "r+") as history:
        history.append({
            "username": username,
            "history": [],
        })

'''
Deletes the user.
Gets username and password in the header of HTTP request.
Returns nothing.
Raises "404 Not Found" if the user doesn't exist.
'''
@app.delete("/users")
async def delete_user(username: str = Header(default=None), password: str = Header(default=None)):
    if not verify_user(username, password):
        raise HTTPException(status_code=404, detail="User not found")

    with JsonContextManager("DB/users.json", "r+") as users:
        user = get_user(username, "DB/users.json")
        users.remove(user)
    with JsonContextManager("DB/history.json", "r+") as history:
        user = get_user(username, "DB/history.json")
        history.remove(user)

'''
Returns the history of users translations.
Gets username and password in the header of HTTP request. Gets quantity as a quantity of request in the history to return (0 by default).
Raises "401 Unauthorized" if the username or password is incorrect.
Raises "400 Bad Request" if the quantity is invalid.
'''
@app.get("/history")
async def get_history(username: str = Header(default=None), password: str = Header(default=None), quantity: str = Query(default='0')):
    if not verify_user(username, password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = get_user(username, "DB/history.json")

    if 'all' in quantity:
        return user["history"]

    quantity = int(quantity)
    greater_than_zero = quantity > 0
    less_or_equal = quantity <= len(user["history"])
    if greater_than_zero and less_or_equal:
        slice_start = len(user["history"]) - quantity
        return user["history"][slice_start:]

    raise HTTPException(status_code=400, detail="Invalid quantity")


'''
Deletes the history of users translations.
Gets username and password in the header of HTTP request.
Returns nothing.
Raises "404 Not Found" if the user doesn't exist.
'''
@app.delete("/history")
async def delete_user_history(username: str = Header(default=None), password: str = Header(default=None)):
    if not verify_user(username, password):
        raise HTTPException(status_code=404, detail="User not found")

    with JsonContextManager("DB/history.json", "r+") as history:
        user = get_user(username, "DB/history.json")
        index = history.index(user)
        user["history"].clear()
        history[index] = user