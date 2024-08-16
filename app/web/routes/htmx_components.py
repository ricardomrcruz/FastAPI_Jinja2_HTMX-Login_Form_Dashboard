from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["htmx components"])

templates = Jinja2Templates(directory="templates")

def render_template(request: Request, template_name: str):
    return templates.TemplateResponse(request, name=template_name)

@router.get("/dropdown-feat", response_class=HTMLResponse)
async def dropdown_feat(request: Request):
    return render_template(request,"partials/dropdown-feat.html" )

@router.get("/dropdown-about", response_class=HTMLResponse)
async def dropdown_about(request: Request):
    return render_template(request,"partials/dropdown-about.html" )
   
@router.get("/register_form", response_class=HTMLResponse)
async def register_form(request: Request):
    return render_template(request, "components/register_form.html")

@router.get("/toggle_sidenav", response_class=HTMLResponse)
async def toggle_sidenav(request:Request):
    return render_template(request, "partials/toggle-sidenav.html")

@router.get("/recent_search", response_class=HTMLResponse)
async def toggle_sidenav(request:Request):
    return render_template(request, "partials/recent-search.html")
    
@router.get("/sidenav", response_class=HTMLResponse)
async def sidenav(request: Request):
    return render_template(request, "components/sidenav.html")

@router.get("/empty", response_class=HTMLResponse)
async def empty():
    return ""

