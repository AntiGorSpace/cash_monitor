select 
    *
from
    users
where
    lower(login) = lower(:login) AND
    password_hash = crypt(:password, password_hash)