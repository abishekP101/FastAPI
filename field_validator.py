from pydantic import BaseModel , EmailStr , AnyUrl , Field , field_validator , model_validator ,computed_field
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    email: EmailStr
    # married: bool
    # allergies: List[str]
    contact : Dict[str , str]

    @field_validator('email')
    @classmethod
    def email_validator(cls , value):
        valid = ['hdfc.com' ,'icici.com']

        domain_name = value.split('@')[-1]

        if domain_name not in valid:
            raise ValueError('Not a valid domain')
        
        return value

    @model_validator(mode='after')
    def validate_emergency_contact(cls , model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError('Missing emergency contact')
        return model
    
    @computed_field
    @property

    def bmi(self) -> float:
        bmi = round(self.weight/(self.height)**2 , 2)
        return bmi


patient1 = {'name':'Abishek','age':89 ,'weight':12.2 ,'height':13, 'email':'abishek@hdfc.com' ,'contact':{'mummmy':'123' ,'emergency':'1222'}}

p = Patient(**patient1)
print(p)
