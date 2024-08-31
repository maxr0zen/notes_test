# app/main.py
from datetime import timedelta
from typing import List

from fastapi.openapi.models import Response
from jose import JWTError, jwt
from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from models import note_collection, Note
from schemas import User, Token, NoteInDB, NoteUpdate, NoteCreate, TokenData
from crud import create_user, get_user, delete_note, update_note, get_note, get_notes, create_note, get_current_user, \
    check_spelling
from security import create_access_token, verify_password, decode_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, \
    ALGORITHM, oauth2_scheme

app = FastAPI()


@app.post("/register")
async def register(user: User):
    existing_user = await get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    await create_user(user)
    return {"message": "User registered successfully"}


@app.post("/login", response_model=Token)
async def login(user: User):
    stored_user = await get_user(user.username)
    if not stored_user:
        raise HTTPException(status_code=401, detail="User not registered")
        if not verify_password(user.password, stored_user["password"]):
            raise HTTPException(status_code=401, detail="Wrong password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Здесь вы должны проверить данные пользователя и вернуть JWT токен
    return {"access_token": "example_token", "token_type": "bearer"}







@app.post("/notes/", response_model=NoteInDB)
async def create_new_note(note: NoteCreate, owner: str = Depends(get_current_user)):
    note.title = await check_spelling(note.title)
    note.content = await check_spelling(note.content)

    new_note = await create_note(owner, note.dict())
    return new_note

@app.get("/notes/", response_model=List[NoteInDB])
async def read_notes(owner: str = Depends(get_current_user)):
    notes = await get_notes(owner)
    return notes

@app.get("/notes/{note_id}", response_model=NoteInDB)
async def read_note(note_id: str, owner: str = Depends(get_current_user)):
    note = await get_note(note_id, owner)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=NoteInDB)
async def update_existing_note(note_id: str, note: NoteUpdate, token: str = Depends(get_current_user)):
    owner = token
    note.title = await check_spelling(note.title)
    note.content = await check_spelling(note.content)

    updated_note = await update_note(note_id, owner, note.dict())
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    updated_note_data = await update_note(note_id, owner, note.dict())

    if not updated_note_data:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")

    # Формируем объект заметки для возврата в ответе
    updated_note = NoteInDB(
        id=note_id,
        title=updated_note_data['title'],
        content=updated_note_data['content'],
        owner=owner  # Владелец устанавливается на основе текущего аутентифицированного пользователя
    )
    return updated_note

@app.delete("/notes/{note_id}", response_model=dict)
async def delete_existing_note(note_id: str, owner: str = Depends(get_current_user)):
    success = await delete_note(note_id, owner)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return {"message": "Note deleted successfully"}