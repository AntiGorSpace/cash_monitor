from databases import Database
from core.config import POSTGRES_URL
from fastapi.templating import Jinja2Templates


database = Database(POSTGRES_URL)

requests = Jinja2Templates(directory="db")

def get_sql(path:str, params:dict={}) -> str:
    return requests.get_template(f'sql/{path}.sql').render( **params )

    
    