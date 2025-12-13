from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

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

 
    

