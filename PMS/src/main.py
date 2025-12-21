from fastapi import FastAPI
from PatientManagement.routes import patient_router
from contextlib import asynccontextmanager
from db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is started... ")
    await init_db()
    yield
    print(f"Server has been stopped ")

version = 'v1'
app = FastAPI(
    title="PMS",
    description='A REST API for a book review web services',
    version=version,
    lifespan=life_span
)
app.include_router(patient_router)
