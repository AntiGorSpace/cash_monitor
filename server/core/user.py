from core.config import CURRENCY_API_KEY
from aiohttp import ClientSession
from datetime import datetime

from .base import BaseRepository
from db.base import get_sql
from models.users import ShowUser, UserLogin


class UserClass(BaseRepository):
	
	async def login(self, login_data:UserLogin) -> ShowUser | None :
		res = await self.database.fetch_one( 
			get_sql('User/login'),
			{
				'login':login_data.login,
				'password':login_data.password
			}
		)
		return ShowUser.parse_obj(res) if res else None
	
	async def get_by_id(self, user_id:int) -> ShowUser | None :
		res = await self.database.fetch_one( 
			'select * from users where id=:user_id',
			{ 'user_id':user_id }
		)
		return ShowUser.parse_obj(res) if res else None

	async def set_base_currency(self, user_id:int, code:str):
		await self.database.execute( 
			'update users set base_code_id = (select id from currencies where code = :code) where id = :user_id',
			{ 
				'user_id':user_id,
				'code': code
			}
		)
		
