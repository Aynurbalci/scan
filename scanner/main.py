from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import config
import sys
sys.path.insert(0, str(config.ROOT_DIR))
from scanner.api.endpoints.items import router

app = FastAPI()


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=templates.TemplateResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(router, prefix="/upload", tags=["upload"])

