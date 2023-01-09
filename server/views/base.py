from fastapi.templating import Jinja2Templates
from json import load as json_load
from fastapi import Request


templates = Jinja2Templates(directory="views")

def get_lang_json(folder:str, lang_code:str) -> dict:
	with open(f"views/{folder}/lang.json", "r", encoding='utf-8') as read_content:
		lang_json = json_load(read_content)
	lang = {}
	for k in lang_json: lang[k] = lang_json[k][lang_code] if lang_code in lang_json[k] else lang_json[k]['ru']
	return lang

def get_view(request: Request, folder:str, view_name:str='item', additional_data:dict = {}):
	lang_code = request.cookies['lang'] if 'lang' in request.cookies else 'en'
	lang_dict = get_lang_json(folder, lang_code)
	m_lang_dict = get_lang_json('main', lang_code)
	view_data = {"request": request, "L":lang_dict, "ML":m_lang_dict}
	view_data.update(additional_data)
	return templates.TemplateResponse(f"{folder}/{view_name}.html", view_data)


	