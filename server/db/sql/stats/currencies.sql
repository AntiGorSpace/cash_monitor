select 
    array_agg(c.code) as codes,
    coalesce(
        max(c.code) FILTER(where u.id is not null),
        'USD'
    ) as base_code,
    coalesce(
        (
            select 
                array_agg(t.code)
            from(
                select 
                    c.code
                from
                    wallets as w
                    left join currencies as c on c.id = w.currency_id
                where
                    w.user_id = :user_id
                group by
                    c.code
            ) as t
        ),
        (
            select 
                array_agg(t.code)
            from(
                select 
                    c.code
                from
                    wallets as w
                    left join currencies as c on c.id = w.currency_id
                group by
                    c.code
                order by count(*) desc
                limit 5
            ) as t
        )
    ) as wallet_codes
from 
    currencies as c  
    left join users as u on u.base_code_id = c.id and u.id = :user_id

    