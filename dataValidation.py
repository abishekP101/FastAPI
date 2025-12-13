from pydantic import BaseModel , EmailStr , AnyUrl , Field
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):
    name : Annotated[str , Field(max_length=50 , title='Name of the patient' , description="Name under 50 words")]
    age  : int = Field(gt=0 , lt=120)
    email : EmailStr
    linkedln : AnyUrl
    weight: Annotated[float , Field(gt=0 , strict=True)]
    married: Annotated[bool , Field(default=None , description='maritial_status')]
    allergies: Optional[List[str]] = Field(default=None , max_length=5)
    contact: Dict[str , str]


patient_info = {'name':'Abishek' , 'age':12 , 'weight':12.1 , 'married':True  , 'contact':{'phone':'123456'}}

patient1  = Patient(**patient_info)

print(patient1)