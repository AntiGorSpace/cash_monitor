from datetime import datetime
from fastapi import Request

from .base import BaseRepository
from views.base import get_view
from db.base import get_sql
from models.users import ShowUser
from models.stats import Codes

import json


class Pages(BaseRepository):
	async def index(self, request:Request, current_user:ShowUser):
		currencies = await self.database.fetch_one(
			get_sql('stats/currencies'),
			{
				'user_id': current_user.id if current_user else 0
			}
		)
		currencies = Codes.parse_obj(currencies)

		additional_data = {
			'currency_codes': currencies.codes,
			'base_code': currencies.base_code,
			'wallet_codes': currencies.wallet_codes
		}
		if current_user:
			additional_data['current_user_login'] = current_user.login
			additional_data['current_user_id'] = current_user.id
		return get_view(request, 'index', additional_data = additional_data)
