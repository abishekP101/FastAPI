from fastapi import APIRouter
from fastapi.responses import JSONResponse 
from fastapi import  Path, HTTPException, Query
import json
from PatientManagement.schema import Patient , PatientUpdate

patient_router = APIRouter()


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json' , 'w') as f:
        json.dump(data , f)

@patient_router.get("/")
def hello():
    return {'message':'Patient Management System API'}

@patient_router.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@patient_router.get('/view')
def view():
    data = load_data()
    return data

@patient_router.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient (example = P001)')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404 , detail='Patient not found')

@patient_router.get('/sort')
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

@patient_router.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400 , detail='Patient already exits')
    else:
        data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201 , content={'message':'patient created successfully...'})

@patient_router.put('/edit/{patient_id}')
def update_patient(patient_id: str , patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail='Patient Not found')
    
    existing_patient_info = data[patient_id]

    updated = patient_update.model_dump(exclude_unset=True)

    for key , value in updated.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump()

    data['patient_id'] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200 , content='Patient updated')



@patient_router.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200 , content={'message':'patient deleted'})