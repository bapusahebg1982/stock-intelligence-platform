from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_stock import router as stock_router
from api.routes_sector import router as sector_router
from api.routes_scanner import router as scanner_router
from api.routes_news import router as news_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_router)
app.include_router(sector_router)
app.include_router(scanner_router)
app.include_router(news_router)
