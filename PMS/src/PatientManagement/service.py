from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from PatientManagement.models import Patient as PatientModel
from PatientManagement.schema import PatientCreateModel, PatientUpdate


class PatientService:
    
    # --------------------------------------------------------
    # 1. Get all patients
    # --------------------------------------------------------
    async def get_all_patient(self, session: AsyncSession):
        stmt = select(PatientModel)
        result = await session.exec(stmt)
        return result.all()

    # --------------------------------------------------------
    # 2. Get one patient by UUID
    # --------------------------------------------------------
    async def get_patient(self, patient_uuid: str, session: AsyncSession):
        patient = await session.get(PatientModel, patient_uuid)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    # --------------------------------------------------------
    # 3. Create new patient  ✅ FIXED VERSION
    # --------------------------------------------------------
    async def create_patient(self, patient_data: PatientCreateModel, session: AsyncSession):
        
        # DO NOT check for patient_data.id (it doesn't exist)
        # UUID will be auto-generated, so no need to check for duplicates.

        new_patient = PatientModel(**patient_data.model_dump())
        
        session.add(new_patient)
        await session.commit()
        await session.refresh(new_patient)

        return new_patient

    # --------------------------------------------------------
    # 4. Update patient by UUID
    # --------------------------------------------------------
    async def update_patient(self, patient_uuid: str, update_data: PatientUpdate, session: AsyncSession):

        patient = await session.get(PatientModel, patient_uuid)

        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        updated_fields = update_data.model_dump(exclude_unset=True)

        for key, value in updated_fields.items():
            setattr(patient, key, value)

        session.add(patient)
        await session.commit()
        await session.refresh(patient)

        return patient

    # --------------------------------------------------------
    # 5. Delete patient by UUID
    # --------------------------------------------------------
    async def delete_patient(self, patient_uuid: str, session: AsyncSession):

        patient = await session.get(PatientModel, patient_uuid)

        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        await session.delete(patient)
        await session.commit()

        return {"message": "Patient deleted successfully"}
