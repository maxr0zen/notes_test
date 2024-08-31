from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteInDB(NoteBase):
    id: str
    owner: str