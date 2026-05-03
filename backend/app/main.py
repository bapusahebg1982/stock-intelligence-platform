import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# -----------------------------
# CORS (VERY IMPORTANT)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# SAFE ROUTER IMPORTS
# -----------------------------
try:
    from api.routes_stock import router as stock_router
    app.include_router(stock_router)
    print("✅ stock router loaded")
except Exception as e:
    print("❌ stock router failed:", e)

try:
    from api.routes_sector import router as sector_router
    app.include_router(sector_router)
    print("✅ sector router loaded")
except Exception as e:
    print("❌ sector router failed:", e)

try:
    from api.routes_scanner import router as scanner_router
    app.include_router(scanner_router)
    print("✅ scanner router loaded")
except Exception as e:
    print("❌ scanner router failed:", e)

try:
    from api.routes_news import router as news_router
    app.include_router(news_router)
    print("✅ news router loaded")
except Exception as e:
    print("❌ news router failed:", e)

# ✅ NEW SEARCH ROUTER
try:
    from api.routes_search import router as search_router
    app.include_router(search_router)
    print("✅ search router loaded")
except Exception as e:
    print("❌ search router failed:", e)


# -----------------------------
# ROOT + HEALTH
# -----------------------------
@app.get("/")
def root():
    return {"status": "running"}

@app.on_event("startup")
def startup_log():
    print("🚀 APP STARTED")

    if os.getenv("GEMINI_API_KEY"):
        print("✅ GEMINI KEY FOUND")
    else:
        print("⚠️ GEMINI KEY MISSING (fallback mode)")
