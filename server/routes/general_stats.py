from typing import List
from fastapi import APIRouter, Depends, UploadFile
from .depends import get_general_stat_class
from core.general_stat import GeneralStat
from models.stats import Currency, CurrencyRates
from datetime import datetime, timedelta
router = APIRouter()

@router.get( '/currency_list', response_model = List[Currency] )
async def currency_list( stats: GeneralStat = Depends(get_general_stat_class) ):
	return await stats.currency_list()

@router.get( '/currency_history', response_model = List[CurrencyRates] )
async def currency_history( 
		stats: GeneralStat = Depends(get_general_stat_class),
		base_currency:str = 'USD',
		timestamp_start = (datetime.today() - timedelta(days=30)).timestamp(), 
		timestamp_end = datetime.today().timestamp()
	):
	return await stats.currency_history( timestamp_start, timestamp_end, base_currency)
