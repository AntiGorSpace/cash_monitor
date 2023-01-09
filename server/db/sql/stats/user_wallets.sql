SELECT
    w.id,
    c.code as currency_code,
    w.name,
    coalesce(cash.value, 0) as value,
    coalesce(cash.value / cr.rate * bcr.rate, 0) as base_value
from
    wallets as w
    left join currencies as c on c.id = w.currency_id
    left join lateral(
        select
            sum(wc.value) as value
        from
            wallet_cash as wc
        where
            wc.wallet_id = w.id
    ) as cash on true
    left join lateral(
        select
            cr.uahvalue as rate
        from
            currency_rates as cr
        where
            cr.currency_id = c.id
        order by 
            cr.actual_date desc
        limit 1
    ) as cr on true

    left join (
        select
            cr.uahvalue as rate
        from
            users as u
            left join currency_rates as cr on cr.currency_id = u.base_code_id
        where
            u.id = :user_id
        order by 
            cr.actual_date desc
        limit 1
    ) as bcr on true
where
    w.user_id = :user_id