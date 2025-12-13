from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state : str
    pin: int

class Patient(BaseModel):
    name : str
    gender: str
    address: Address

address_dict = {'city':'Tadong' , 'state':'Sikkim', 'pin':737102}

ad = Address(**address_dict)

patient_dict = {'name':'Abishek' , 'gender':'male','address': ad}

p = Patient(**patient_dict)
print(p)

temp = p.model_dump(include=['name','gender'])
print(temp)