from pydantic import BaseModel
from typing import List

class RoleBase(BaseModel):
    code: str
    name: str

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    employee_id: str
    name: str
    login: str
    picture: str
    first_name: str
    surname: str
    patronymic: str
    birthday: str
    phone: str


class User(UserBase):
    id: int
    roles: List[Role] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
