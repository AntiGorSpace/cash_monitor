from starlette.config import Config


config = Config('.env')


user = config("POSTGRES_USER", cast=str, default="")
password = config("POSTGRES_PASSWORD", cast=str, default="")
name = config("POSTGRES_DB", cast=str, default="")
port = config("POSTGRES_PORT", cast=str, default="")
host = config("POSTGRES_HOST", cast=str, default="")
POSTGRES_URL = f"postgresql://{user}:{password}@{host}:{port}/{name}"


ACCESS_TOKEN_EXPIRE_DAYS = config("ACCESS_TOKEN_EXPIRE_DAYS", cast=float, default=30)
HASH_KEY = config("HASH_KEY", cast=str, default="")
ROOT_PATH = config("ROOT_PATH", cast=str, default="/")

BOT_KEY = config("BOT_KEY", cast=str, default="")
CURRENCY_API_KEY = config("CURRENCY_API_KEY", cast=str, default="")