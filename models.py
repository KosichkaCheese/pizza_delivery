from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import Optional

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