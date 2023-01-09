from typing import List
from fastapi import APIRouter, Depends
from .depends import get_personal_stat_class, get_current_user
from core.personal_stat import PersonalStat
from models.stats import *
from models.users import *
router = APIRouter()

@router.post( '/add_wallet', response_model = Wallet )
async def add_wallet( 
		params: AddWallet,
		stats: PersonalStat = Depends(get_personal_stat_class) ,
		current_user: ShowUser = Depends(get_current_user)
	):
	return await stats.add_wallet(current_user.id, params)

@router.post( '/del_wallet' )
async def del_wallet( 
		params: DelWallet,
		stats: PersonalStat = Depends(get_personal_stat_class) ,
		current_user: ShowUser = Depends(get_current_user)
	):
	return await stats.del_wallet(current_user.id, params.wallet_id)

@router.post( '/add_cash_to_wallet' )
async def add_cash_to_wallet( 
		params: AddWalletCash,
		stats: PersonalStat = Depends(get_personal_stat_class) ,
		current_user: ShowUser = Depends(get_current_user)
	):
	return await stats.add_cash_to_wallet(current_user.id, params)


@router.get( '/wallets', response_model = List[Wallet] )
async def get_wallets( 
		stats: PersonalStat = Depends(get_personal_stat_class) ,
		current_user: ShowUser = Depends(get_current_user)
	):
	return await stats.get_wallets(current_user.id)
