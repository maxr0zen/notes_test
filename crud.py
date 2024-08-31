from typing import Optional

import httpx
from bson import ObjectId
from jose import jwt, JWTError
from starlette import status

from security import oauth2_scheme, SECRET_KEY, ALGORITHM
from models import user_collection, note_collection
from schemas import User, TokenData
import bcrypt

async def create_user(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    result = await user_collection.insert_one(user_dict)
    return result.inserted_id

async def get_user(username: str):
    user = await user_collection.find_one({"username": username})
    return user

async def get_user_by_id(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return user

async def create_note(owner: str, note: dict) -> dict:
    note["owner"] = owner
    result = await note_collection.insert_one(note)
    note_id = result.inserted_id
    return {**note, "id": str(note_id)}

async def get_notes(owner: str) -> list:
    notes = await note_collection.find({"owner": owner}).to_list(None)
    for note in notes:
        note["id"] = str(note["_id"])
        del note["_id"]
    return notes

async def get_note(note_id: str, owner: str) -> Optional[dict]:
    note = await note_collection.find_one({"_id": ObjectId(note_id), "owner": owner})
    if note:
        note["id"] = str(note["_id"])
        del note["_id"]
    return note

async def update_note(note_id: str, owner: str, updated_note: dict) -> Optional[dict]:
    result = await note_collection.update_one(
        {"_id": ObjectId(note_id), "owner": owner},
        {"$set": updated_note}
    )
    if result.matched_count:
        return {**updated_note, "id": note_id}
    return None

async def delete_note(note_id: str, owner: str) -> bool:
    result = await note_collection.delete_one({"_id": ObjectId(note_id), "owner": owner})
    return result.deleted_count > 0

from fastapi import HTTPException, Depends


async def check_spelling(text: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://speller.yandex.net/services/spellservice.json/checkText",
                params={"text": text, "lang": "ru,en"}
            )
            response.raise_for_status()  # Поднимет исключение для ошибок HTTP
            corrections = response.json()

        # Применяем исправления к тексту
        for correction in corrections:
            word_with_error = correction["word"]
            corrected_word = correction["s"][0] if correction["s"] else word_with_error
            text = text.replace(word_with_error, corrected_word)

        return text
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail="Ошибка при обращении к Яндекс.Спеллеру")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Расшифровка токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data.username

