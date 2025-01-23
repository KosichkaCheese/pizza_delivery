from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Order(BaseModel):
    user_email: str
    time: datetime
    summ: float
    status: Optional[int] = None
