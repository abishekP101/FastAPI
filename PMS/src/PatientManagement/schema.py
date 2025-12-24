from pydantic import BaseModel , Field, computed_field
from typing import Annotated, Literal  , Optional
import uuid


class Patient(BaseModel):
    uid: Annotated[uuid.UUID , Field(..., description='ID of the patient')]
    name: Annotated[str , Field(..., description='Name of the patient')]
    city: Annotated[str , Field(... , description='city of the patient')]
    age: Annotated[int  , Field(... , gt=0 , lt=120 , description='Age of the patient')]
    gender: Annotated[Literal['male' , 'female' , 'others'], Field(... , description='gender of the patient')]
    height : Annotated[float , Field(... ,gt=0, description='Height of the patient in mtrs')]
    weight : Annotated[float , Field(... , gt=0 , description='Weight of the patient in kgs')]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2) , 2)
        return bmi
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 30:
            return 'normal'
        else:
            return 'overweight'

class PatientCreateModel(BaseModel):
    name: Annotated[str , Field(..., description='Name of the patient')]
    city: Annotated[str , Field(... , description='city of the patient')]
    age: Annotated[int  , Field(... , gt=0 , lt=120 , description='Age of the patient')]
    gender: Annotated[Literal['male' , 'female' , 'others'], Field(... , description='gender of the patient')]
    height : Annotated[float , Field(... ,gt=0, description='Height of the patient in mtrs')]
    weight : Annotated[float , Field(... , gt=0 , description='Weight of the patient in kgs')]


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str] , Field(default=None)]
    city: Annotated[Optional[str] , Field(default=None)]
    age: Annotated[Optional[int] , Field(default=None , gt=0)]
    gender: Annotated[Optional[Literal['male','female','others']] , Field(default=None)]
    height: Annotated[Optional[float] , Field(default=None , gt=0)]
    weight: Annotated[Optional[float] , Field(default=None ,gt=0)]
