
with UAH_rates as (
    select 
        upper(key::varchar) as code,
        (value::varchar)::float as rate
    from
        json_each(:rates)
),
new_currencies as (
    insert into currencies (code)
    select
        code
    from
        UAH_rates
    where
        code not in (select code from currencies )
    RETURNING *
)
insert into currency_rates (currency_id, actual_date, uahvalue)
select
    coalesce((select id from currencies as c where c.code = ua.code), (select id from new_currencies as c where c.code = ua.code)),
    TO_DATE(:date,'YYYY-MM-DD'),
    rate
from
    UAH_rates as ua
on conflict do NOTHING