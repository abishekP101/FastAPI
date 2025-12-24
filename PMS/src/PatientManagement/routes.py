from fastapi import APIRouter, Depends
from db.main import get_session
from PatientManagement.service import PatientService
from PatientManagement.schema import PatientCreateModel, PatientUpdate

patient_router = APIRouter()
service = PatientService()

@patient_router.get("/patients")
async def list_patients(session=Depends(get_session)):
    return await service.get_all_patient(session)

@patient_router.get("/patient/{patient_id}")
async def get_patient(patient_id: str, session=Depends(get_session)):
    return await service.get_patient(patient_id, session)

@patient_router.post("/create")
async def create(patient: PatientCreateModel, session=Depends(get_session)):
    return await service.create_patient(patient, session)

@patient_router.put("/edit/{patient_id}")
async def update(patient_id: str, data: PatientUpdate, session=Depends(get_session)):
    return await service.update_patient(patient_id, data, session)

@patient_router.delete("/delete/{patient_id}")
async def delete(patient_id: str, session=Depends(get_session)):
    return await service.delete_patient(patient_id, session)
