SELECT
    c.code,
    c.id,
    json_agg(
        json_build_object(
            'date', cr.actual_date::timestamp,
            'value', cr.uahvalue / bcr.uahvalue
        ) order by cr.actual_date
    ) as history
from
    currency_rates as cr
    left join currencies as c on c.id = cr.currency_id
    left join lateral (
        select
            uahvalue
        from
            currency_rates as bcr
        where
            bcr.actual_date<=cr.actual_date and
            currency_id = (select id from currencies where code=:base_currency)
        order by bcr.actual_date DESC
        limit 1
    ) as bcr on true
where
    cr.actual_date >= TO_DATE(:timestamp_start,'YYYY-MM-DD') AND
    cr.actual_date <= TO_DATE(:timestamp_end,'YYYY-MM-DD')
group BY
    c.id