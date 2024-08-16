from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,  RedirectResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from datetime import datetime, timezone

from app.core.security import AuthHandler
from app.db.session import engine
from app.models.user import User as Userdb
from app.db.session import get_session

from app.crud.user import (
    create_user
)
from app.models.user import UserCreate

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="templates")
auth_handler = AuthHandler()


# routes

@router.post("/register/", response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    verify_password: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    
    if verify_password != password:
            logger.info(f"Error. Passwords dont verify eachother.")
            return HTMLResponse(
                content="<p class='text-red-600 '>Passwords don't match. Please retry.</p>",
                status_code=422,
            )
    hashed_password = auth_handler.get_hash_password(password)      
    current_time= datetime.now(timezone.utc)
        
    user = UserCreate(
        email=email,
        username=username, 
        hashed_password=hashed_password,
        is_active=True,
        updated_at=current_time,
        )
    
    try:
        await create_user(session, user)
        response = templates.TemplateResponse({"request": request}, name="login.html")
        response.headers["HX-Location"] = "/signin"
        return response
    except HTTPException as e:
        return HTMLResponse(
            content="<p class='text-red-600 '>Registration failed. Check email and username.</p>",
            status_code=409,
        )
        
@router.post("/login/")
async def sign_in(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    try:
        logger.info(f"Attempting to find user with email: {email}")
        # find user mail
        query = select(Userdb).where(Userdb.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            logger.info(f"This email is not registered.")
            return HTMLResponse(
            content="<p class='text-red-600 '>This email is not registered.</p>",
            status_code=404,
        )

        logger.info(f"User found: {user.email}")

        authenticated_user = await auth_handler.authenticate_user(email, password)
        if authenticated_user:
            # if user and password verifies create cookie
            atoken = auth_handler.create_access_token(user.email)
            logger.info(
                f"Authentication successful for user: {user.email}. Redirecting to dashboard."
            )
            response = templates.TemplateResponse(
                    {"request": request}, name="dashboard.html"
            )
            response.headers["HX-Redirect"] = "/dashboard"
            response.set_cookie(
                key="Authorization", value=f"{atoken}", httponly=True
            )
            response.set_cookie(key="welcome", value="welcome back to Mark3ts")
            return response
        else:
            logger.info(f"The password is invalid.")
            return HTMLResponse(
                content="<p class='text-red-600 '>The password is invalid.</p>",
                status_code=401,
            )
    except Exception as err:    
        logger.info(f"An unexpected error occurred: {err}")
        return HTMLResponse(
            content="<p class='text-red-600 '>Theres an error with the form submission.</p>",
            status_code=500,
        )


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = templates.TemplateResponse({"request": request}, name="index.html")
    response.delete_cookie("Authorization")
    return response


