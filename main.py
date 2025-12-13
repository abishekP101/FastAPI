from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel , Field, computed_field
from typing import Annotated, Literal 


app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str , Field(..., description='ID of the patient')]
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


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json' , 'w') as f:
        json.dump(data , f)

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient (example = P001)')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404 , detail='Patient not found')

@app.get('/sort')
def sort_required(sort_by: str = Query(... , description='sort on the basis of height , weight and bmi') ,
                   order: str = Query('asc', description='Ascending and  descending order')):
    
    sort_field= ['height' , 'weight' , 'bmi']

    if sort_by not in sort_field:
        raise HTTPException(status_code=400 , detail=f'Invalid field: choose from {sort_field}')
    
    order_field = ['asc' , 'dsc']
    
    if order not in order_field:
        raise HTTPException(status_code=400 , detail=f'Invalid field: choose from {order_field}')
    
    data = load_data()
    sort_order = True if order== 'dsc' else False

    sorted_data = sorted(data.values() , key= lambda x: x.get(sort_by , 0) , reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400 , detail='Patient already exits')
    else:
        data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201 , content={'message':'patient created successfully...'})

    

