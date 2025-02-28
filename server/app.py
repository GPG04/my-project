from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import bcrypt
salt = bcrypt.gensalt()

from db import *

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

@app.get("/users/{user_id}")
def getUser(user_id: int):
    try:
        cursor.execute("SELECT * FROM Users WHERE id = %s;", (user_id,))
        return cursor.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

@app.post("/users")
def postUser(user: User):
    try:
        hash = bcrypt.hashpw(user.password, salt)
        cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s) RETURNING *;", (user.username, hash))
        db.commit()
        return cursor.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

@app.put("/users/{user_id}")
def updateUser(user_id: int, user: User):
    try:
        hash = bcrypt.hashpw(user.password, salt)
        cursor.execute("""
                       UPDATE Users SET username=%(username)s, password=%(password)s WHERE id=%(id)s RETURNING *;""",
                        {'username': user.username, 'password': hash, 'id': user_id})
        db.commit()
        return cursor.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

@app.delete("/users/{user_id}")
def deleteUser(user_id):
    try:
        SQL = ("DELETE FROM Users WHERE id=%s;")
        data = (user_id)
        cursor.execute(SQL, data)
        db.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

@app.post("/auth/login")
def authenticate(user: User):
    try:
        cursor.execute("SELECT password FROM Users WHERE username=%s;", (user.username,))
        res: bytes
        (res,) = cursor.fetchone()
        print(res)
        print(bcrypt.checkpw(user.password, res))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)