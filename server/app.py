from typing import Union, Annotated

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt

import bcrypt
salt = bcrypt.gensalt()

from db import *

load_dotenv()
key = os.getenv("JWT_SECRET")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class User(BaseModel):
    username: str
    password: bytes
    is_admin: Union[bool, None] = None

@app.get("/users")
def getUsers():
    try:
        cursor.execute("SELECT * FROM Users;")
        return cursor.fetchmany()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.get("/users/{user_id}")
def getUser(user_id: int):
    try:
        cursor.execute("SELECT * FROM Users WHERE id = %s;", (user_id,))
        (id, username, password, is_admin) = cursor.fetchone()
        return {"id": id, "username": username, "password": password, "is_admin": is_admin}
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.post("/users")
def postUser(user: User):
    try:
        hash = bcrypt.hashpw(user.password, salt)
        SQL = ("INSERT INTO Users (username, password) VALUES (%s, %s) RETURNING *;")
        data = (user.username, hash)
        cursor.execute(SQL, data)
        db.commit()
        (id, username, password, is_admin) = cursor.fetchone()
        return {"id": id, "username": username, "password": password, "is_admin": is_admin}
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.put("/users/{user_id}")
def updateUser(user_id: int, user: User):
    try:
        hash = bcrypt.hashpw(user.password, salt)
        cursor.execute("""
                       UPDATE Users SET username=%(username)s, password=%(password)s WHERE id=%(id)s RETURNING *;""",
                        {'username': user.username, 'password': hash, 'id': user_id})
        db.commit()
        (id, username, password, is_admin) = cursor.fetchone()
        return {"id": id, "username": username, "password": password, "is_admin": is_admin}
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.delete("/users/{user_id}")
def deleteUser(user_id):
    try:
        SQL = ("DELETE FROM Users WHERE id=%s;")
        data = (user_id)
        cursor.execute(SQL, data)
        db.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.post("/auth/login")
def authenticate(user: User):
    try:
        cursor.execute("SELECT id, password FROM Users WHERE username=%s;", (user.username,))
        res: bytes
        (user_id, res) = cursor.fetchone()
        if bcrypt.checkpw(user.password, res) == False:
            raise Exception("Error Logging In")
        Token = jwt.encode({"id":user_id}, key, algorithm="HS256")
        print(Token)
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.get("/auth/me")
async def isLoggedIn(Token: Annotated[str | None, Header()] = None):
    try:
        res = jwt.decode(Token, key, algorithms="HS256")
        id = res["id"]
        cursor.execute("SELECT * FROM Users WHERE id=%s;", (id,))
        print(cursor.fetchone())
    except (Exception, psycopg.DatabaseError) as error:
        print(error)