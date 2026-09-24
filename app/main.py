from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models  # noqa: F401
from .routers import auth as auth_router
from .routers import medicines as medicines_router
from .routers import hydration as hydration_router
from .routers import routine as routine_router
from .routers import appointments as appointments_router
from .routers import difficulty as difficulty_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CogniCare API",
    description="Backend for CogniCare elder care app",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CogniCare API is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-check")
def db_check():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    return {
        "status": "connected",
        "tables": inspector.get_table_names(),
    }


# ─── Routers ────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(medicines_router.router)
app.include_router(hydration_router.router)
app.include_router(routine_router.router)
app.include_router(appointments_router.router)
app.include_router(difficulty_router.router)