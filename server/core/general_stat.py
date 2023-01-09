from datetime import datetime, timedelta
from db.base import get_sql
from typing import List

from .base import BaseRepository
from models.stats import *

class GeneralStat(BaseRepository):
	async def currency_list(self) -> List[Currency]:
		res = await self.database.fetch_all( 'select * from currencies' )
		return list(map(lambda obj: Currency.parse_obj(obj), res))

	async def currency_history(
			self,  
			timestamp_start = (datetime.today() - timedelta(days=30)).timestamp(), 
			timestamp_end = datetime.today().timestamp(),
			base_currency = 'USD' 
		) -> List[CurrencyRates]:
		res = await self.database.fetch_all( 
			get_sql('stats/currency_history'),
			{
				'timestamp_start': datetime.fromtimestamp(float(timestamp_start)).strftime('%Y-%m-%d'),
				'timestamp_end': datetime.fromtimestamp(float(timestamp_end)).strftime('%Y-%m-%d'),
				'base_currency':base_currency
			}
		)
		return list(map(lambda obj: CurrencyRates.parse_obj(obj), res))
	
		


				


