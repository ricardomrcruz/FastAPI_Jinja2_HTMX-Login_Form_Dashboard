import logging
import warnings

logging.basicConfig(level=logging.INFO)
logging.info("FastAPI application starting")

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

from app.core.config import settings
from app.db.utils import create_db_and_tables
from app.db.session import engine
from app.core.security import  RequiresLoginException

warnings.filterwarnings(
    "ignore", category=UserWarning, message=r".*PydanticJsonSchemaWarning.*"
)

logging.info(f"Connecting to database: {engine.url.render_as_string(hide_password=True)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting to create database tables...")
    try:
        await create_db_and_tables(engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
    yield
    logging.info("Application shutting down")
    

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


# redirection from exception to index
@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return RedirectResponse(url="/")


@app.middleware("http")
async def create_auth_header(request: Request, call_next):
    """
    Checks if there are cookies set for authorization. If so, contruct
    the authorization header and modify the request (unless the header
    already exists!)
    """
    if "Authorization" not in request.headers and "Authorization" in request.cookies:
        access_token = request.cookies["Authorization"]

        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer{access_token}".encode(),
            )
        )
    elif (
        "Authorization" not in request.headers
        and "Authorization" not in request.cookies
    ):
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer 1234".encode(),
            )
        )

    response = await call_next(request)
    return response


@app.get("/health", tags=["info"])
async def health():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for api doccumentation",
    )
    

    


    



