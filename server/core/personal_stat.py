from datetime import datetime
from db.base import get_sql
from typing import List

from .base import BaseRepository
from models.stats import *


class PersonalStat(BaseRepository):
	
	async def add_wallet(self,  user_id:int, params:AddWallet) -> Wallet:
		res = await self.database.fetch_one( 
			get_sql('stats/add_wallet'),
			{
				'user_id':user_id,
				'currency_code':params.currency_code,
				'name': params.name
			}
		)
		return Wallet.parse_obj(res)
	
	async def del_wallet(self,  user_id:int, wallet_id:int):
		await self.database.execute( 
			get_sql('stats/delete_wallet'),
			{
				'user_id':user_id,
				'wallet_id':wallet_id
			}
		)
		return {'ok':1}

	async def get_wallets(self, user_id:int) -> List[Wallet]:
		res = await self.database.fetch_all(
			get_sql('stats/user_wallets'),
			{ 'user_id':user_id }
		)
		return list(map(lambda obj: Wallet.parse_obj(obj), res))

	async def add_cash_to_wallet(self, user_id:int, params:AddWalletCash):
		res = await self.database.fetch_one(
			get_sql('stats/add_cash_to_wallet'),
			{ 
				'user_id':user_id,
				'wallet_id':params.wallet_id,
				'value':params.value
			}
		)
		return {'ok':1}
				


