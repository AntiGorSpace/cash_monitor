with del_w_c as (
    delete from wallet_cash where 
        wallet_id = (
            select 
                id 
            from 
                wallets 
            where 
                id = :wallet_id and 
                user_id = :user_id
        )
)

delete from wallets 
where 
    id = :wallet_id and 
    user_id = :user_id