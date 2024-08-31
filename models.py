import os

import jwt
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from typing import Optional, Any, Coroutine, Mapping

from starlette import status

from schemas import TokenData
from security import SECRET_KEY, ALGORITHM

MONGO_DETAILS = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["fastapi_jwt_db"]
user_collection = database["users"]
note_collection = database["notes"]

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"]
    }

def get_user_by_username(username: str) -> Coroutine[Any, Any, Mapping[str, Any] | None | Any]:
    return user_collection.find_one({"username": username})

def get_note_by_id(note_id: str):
    return note_collection.find_one({"_id": ObjectId(note_id)})

class User(BaseModel):
    username: str
    password: str

class Note(BaseModel):
    title: str
    content: str
    owner: str = None

class NoteCreate(Note):
    pass

class NoteUpdate(Note):
    pass

class NoteInDB(BaseModel):
    id: str
    title: str
    content: str
    owner: str




