
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from app.web.routes.pages import router as pages
from app.api.routes import router as api_router
from app.web.routes.htmx_components import router as htmx_router
from app.web.routes.auth import router as auth_router
from app.web.routes.scraper import router as scraper_router

def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        doc_url="/docs", 
        lifespan=lifespan,
    )
    app.include_router(pages)
    app.include_router(api_router, prefix="/api")
    app.include_router(htmx_router)
    app.include_router(auth_router)
    app.include_router(scraper_router)
    return app

app = get_application() 


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/health", tags=["info"])
async def health():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for api doccumentation",
    )
    

    


    



