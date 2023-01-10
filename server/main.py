from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi_utils.tasks import repeat_every

from db.base import database

from models.users import ShowUser

from routes.general_stats import router as general_stat_router
from routes.personal_stats import router as personal_stat_router
from routes.user import router as user_router
from routes.depends import get_outer_api_class, get_current_user, get_pages_class

from core.config import ROOT_PATH
from core.outer_apis import OuterAPIs
from core.pages import Pages


app = FastAPI(root_path = ROOT_PATH)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(general_stat_router, prefix="/api/general_stat", tags=["general_stat"])
app.include_router(personal_stat_router, prefix="/api/personal_stat", tags=["personal_stat"])
app.include_router(user_router, prefix="/api/user", tags=["user"])


@repeat_every(seconds=60 * 60 * 12)
async def remove_expired_tokens_task() -> None:
	outer_apis: OuterAPIs = Depends(get_outer_api_class)
	await outer_apis.load_currency_from_server()

@app.on_event('startup')
async def startup():
	await database.connect()

@app.on_event('shutdown')
async def shutdown():
	await database.disconnect()
	await remove_expired_tokens_task()

@app.get("/", response_class=HTMLResponse)
async def get_form(
		request: Request,
		current_user: ShowUser = Depends(get_current_user),
		pages:Pages = Depends(get_pages_class)
	):
	return await pages.index(request, current_user)
