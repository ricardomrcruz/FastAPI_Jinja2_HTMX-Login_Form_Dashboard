from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.scraper.market1 import scrape as market_scrape

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["scraper"])

templates = Jinja2Templates(directory="templates")


@router.post("/scrape_test")
async def scrape_test(query: str):
    try:
        result = await market_scrape(query)
        return {"data": result}
    except Exception as e:
        logger.error(f"error in scrapetest: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scrape", response_class=HTMLResponse)
async def scrape_general(request: Request, query: str = Form(...)):
    
    try:
        result = await market_scrape(query)

        data = {"data": result}

        return templates.TemplateResponse(
            "components/product_card_3.html", {"request": request, "data": result}
        )

    except Exception as e:
        logger.error(f"error in scrapetest: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
