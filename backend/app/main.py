from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔥 IMPORTANT: import router correctly
from api.routes_bloomberg import router as bloomberg_router
app.include_router(bloomberg_router)
app = FastAPI()

# ---------------------------
# CORS (frontend access)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# ROUTES (THIS WAS MOST LIKELY MISSING)
# ---------------------------
app.include_router(bloomberg_router, prefix="/bloomberg")


# ---------------------------
# HEALTH CHECK (DEBUGGING)
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------
# ROOT
# ---------------------------
@app.get("/")
def root():
    return {"message": "Bloomberg API running"}
