from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,  RedirectResponse

router = APIRouter(tags=["pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse({"request": request}, name="index.html")

@router.get("/signin", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse({"request": request}, name="login.html")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # blocked access without cookie
    auth_token = request.cookies.get("Authorization")
    if not auth_token:
        return RedirectResponse(url="/signin", status_code=302)

    welcome = request.cookies.get("welcome", "")

    response = templates.TemplateResponse(
        {
            "request": request,
            "USERNAME": request.cookies.get("username", "User"),
            "success_login": welcome,
        },
        name="dashboard.html",
    )
    response.delete_cookie("welcome")
    return response

@router.get("/main_search", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse({"request": request}, name="layout/main_search.html")

@router.get("/main_dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse({"request": request}, name="layout/main_dashboard.html")

