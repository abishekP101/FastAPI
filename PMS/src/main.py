from fastapi import FastAPI
from PatientManagement.routes import patient_router

version = 'v1'
app = FastAPI(
    title="PMS",
    description='A REST API for a book review web services',
    version=version
)

app.include_router(patient_router)
