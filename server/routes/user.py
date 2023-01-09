from typing import List
from fastapi import APIRouter, Depends, Response, HTTPException, status
from .depends import get_user_class, get_current_user
from core.user import UserClass
from core.security import create_accsess_token
from models.users import *
router = APIRouter()

@router.post( '/login', response_model = ShowUser )
async def login( 
		response: Response,
		params: UserLogin,
		user: UserClass = Depends(get_user_class),
	):
	u = await user.login(params)
	if u is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect creds')

	response.set_cookie(
		key="sid", 
		value=create_accsess_token({'uid':u.id}), 
		httponly=True, 
		secure=True,
		expires=300000000
	)
	return u

@router.get('/logout')
async def logout(response: Response):
	response.set_cookie( key="sid", value='', httponly=True, secure=True, expires=0 )
	return {'ok':1}

@router.post('/set_base_currency')
async def set_base_currency(
		params: UserBaseCurrency,
		user: UserClass = Depends(get_user_class),
		current_user: ShowUser = Depends(get_current_user)
	):
	if not current_user:
		return {'error':1}	
	await user.set_base_currency(current_user.id, params.code )
	return {'ok':1}

