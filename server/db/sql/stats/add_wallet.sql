insert into wallets (
    user_id, 
    currency_id, 
    name
) values(
    :user_id,
    (select id from currencies where code = :currency_code),
    :name
) RETURNing 
    id, 
    :currency_code as currency_code, 
    name, 
    0 as value, 
    0 as base_value