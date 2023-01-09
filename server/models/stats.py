from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import json

class Currency(BaseModel):
	id:int
	code:str
	no:int | None = None

class Wallet(BaseModel):
	id:int
	currency_code:str
	name:str
	value:float
	base_value:float
	@validator('base_value')
	def result_check(cls, v):
		return round(v, 2)
	
class DateRate(BaseModel):
	date: datetime
	value: float

class CurrencyRates(BaseModel):
	# id:int
	code:str
	history:List[DateRate] = []
	@validator('history', pre=True, always=True)
	def str_to_hash(cls, v): 
		return list(map(lambda el: DateRate.parse_obj(el), json.loads(v))) if type(v) == str else v

class AddWallet(BaseModel):
	currency_code:str
	name:str

class Codes(BaseModel):
	codes: List[str]
	base_code: str
	wallet_codes: List[str]

class AddWalletCash(BaseModel):
	wallet_id:int
	value:float

class DelWallet(BaseModel):
	wallet_id:int
