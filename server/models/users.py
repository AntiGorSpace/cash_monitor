from pydantic import BaseModel
from typing import List


class ShowUser(BaseModel):
	id: int
	login: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserBaseCurrency(BaseModel):
    code: str

