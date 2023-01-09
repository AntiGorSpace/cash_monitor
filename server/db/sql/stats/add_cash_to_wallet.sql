insert into wallet_cash (wallet_id, value) 
select
    id,
    :value
from
    wallets as w
where
    w.user_id = :user_id and
    w.id = :wallet_id
RETURNING *