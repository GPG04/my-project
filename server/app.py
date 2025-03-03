from typing import Union, Annotated

from array import *
from uuid import *
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
        myArr: array[dict] = []
        for (id, username, password, is_admin) in cursor.fetchall():
            myArr.append({"id": id, "username": username, "password": password, "is_admin": is_admin})
        return myArr
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.get("/users/{user_id}")
def getUser(user_id: UUID):
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
        SQL = ("INSERT INTO Users (id, username, password) VALUES (%s, %s, %s) RETURNING *;")
        data = (uuid4(), user.username, hash)
        cursor.execute(SQL, data)
        db.commit()
        (id, username, password, is_admin) = cursor.fetchone()
        return {"id": id, "username": username, "password": password, "is_admin": is_admin}
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.put("/users/{user_id}")
def updateUser(user_id: UUID, user: User, Token: Annotated[str | None, Header()] = None):
    try:
        res = jwt.decode(Token, key, algorithms="HS256")
        id: Union[str | UUID] = res["id"]
        cursor.execute("SELECT is_admin FROM Users WHERE id=%s", (id,))
        (is_admin,) = cursor.fetchone()
        id = UUID(id)

        if id == user_id or is_admin == True:
            hash = bcrypt.hashpw(user.password, salt)
            cursor.execute("""
                        UPDATE Users SET username=%(username)s, password=%(password)s WHERE id=%(id)s RETURNING *;""",
                        {'username': user.username, 'password': hash, 'id': user_id})
            db.commit()
            (id, username, password, is_admin) = cursor.fetchone()
            return {"id": id, "username": username, "password": password, "is_admin": is_admin}
        else:
            raise Exception("Not Authorized!")
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.delete("/users/{user_id}")
def deleteUser(user_id: UUID, Token: Annotated[str | None, Header()] = None):
    try:
        res = jwt.decode(Token, key, algorithms="HS256")
        id: Union[str | UUID] = res["id"]
        cursor.execute("SELECT is_admin FROM Users WHERE id=%s;", (id,))
        (is_admin,) = cursor.fetchone()
        id = UUID(id)

        if user_id == id or is_admin == True:
            cursor.execute("DELETE FROM Users WHERE id=%s;", (user_id,))
            db.commit()
        else:
            raise Exception("Not Authorized!")
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.post("/auth/login")
def authenticate(user: User):
    try:
        cursor.execute("SELECT id, password FROM Users WHERE username=%s;", (user.username,))
        res: bytes
        (user_id, res) = cursor.fetchone()
        id_string = str(user_id)
        if bcrypt.checkpw(user.password, res) == False:
            raise Exception("Error Logging In")
        Token = jwt.encode({"id":id_string}, key, algorithm="HS256")
        print(Token)
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

@app.get("/auth/me")
async def isLoggedIn(Token: Annotated[str | None, Header()] = None):
    try:
        res = jwt.decode(Token, key, algorithms="HS256")
        id: UUID = res["id"]
        cursor.execute("SELECT * FROM Users WHERE id=%s;", (id,))
        (id, username, password, is_admin) = cursor.fetchone()
        return {"id": id, "username": username, "password": password, "is_admin": is_admin}
    except (Exception, psycopg.DatabaseError) as error:
        print(error)