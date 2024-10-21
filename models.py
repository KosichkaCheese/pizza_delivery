from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import Optional
from datetime import datetime

class Usercreate(BaseModel):
    email: EmailStr
    role: Optional[bool]=False
    name: Optional[str]=None
    phone: str
    address: Optional[str]=None

class Useredit(BaseModel):
    email: EmailStr
    name: Optional[str]=None
    phone: Optional[str]=None
    address: Optional[str]=None
    
class Pizza(BaseModel):
    name: str
    cost: float
    description: Optional[str]=None
    image: Optional[str]=None

class Order(BaseModel):
    user_email: str
    time: datetime
    summ: float
    status: Optional[int]=None