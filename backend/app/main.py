import sys
import os

# 🔥 FIX: make backend root visible to Python (Render fix)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_stock import router as stock_router
from api.routes_scanner import router as scanner_router

from database.db import engine
from database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_router)
app.include_router(scanner_router)


@app.get("/")
def root():
    return {"status": "Backend running"}
