from fastapi import Depends, HTTPException,status, Cookie

from db.base import database
from core.outer_apis import OuterAPIs
from core.general_stat import GeneralStat
from core.personal_stat import PersonalStat
from core.pages import Pages
from core.user import UserClass
from models.users import *
from core.security import decode_accsess_token


def get_outer_api_class() -> OuterAPIs:
    return OuterAPIs(database)

def get_general_stat_class() -> GeneralStat:
    return GeneralStat(database)

def get_personal_stat_class() -> PersonalStat:
    return PersonalStat(database)

def get_user_class() -> UserClass:
    return UserClass(database)

def get_pages_class() -> Pages:
    return Pages(database)


async def get_current_user(
    sid:str | None = Cookie(alias='sid', default=None),
	users: UserClass = Depends(get_user_class),
) -> ShowUser | None:
    if sid is None:
        return None
    # cred_exeption = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Creds not valid')
    payload = decode_accsess_token(sid)
    if payload is None:
        # raise cred_exeption
        return None
    id: int = payload["uid"]
    if id is None:
        # raise cred_exeption
        return None
    user = await users.get_by_id(id)
    if user is None:
        # raise cred_exeption
        return None
    return user