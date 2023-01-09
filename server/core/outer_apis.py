from core.config import CURRENCY_API_KEY
from aiohttp import ClientSession
from datetime import datetime

from .base import BaseRepository
from db.base import get_sql
from core.logs import write_log
import json


class OuterAPIs(BaseRepository):
	
	async def load_currency_from_server(self,  date = datetime.now() ):
		str_date = date.strftime('%Y-%m-%d')

		async with ClientSession() as session:
			url = f"https://api.apilayer.com/exchangerates_data/{str_date}?&base=UAH&apikey={CURRENCY_API_KEY}"
			async with session.get(url) as resp:
				data = await resp.json()
				write_log('exchangerates_data', data)
				resp_data = {
					'date': datetime.fromtimestamp(data['timestamp']).strftime('%Y-%m-%d'),
					'rates': json.dumps(data['rates'])	
				}
				print(resp_data)
				await self.database.execute( get_sql('OuterAPIs/save_currency_rates'), resp_data )

				


