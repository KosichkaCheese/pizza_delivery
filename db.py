from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean

ADMIN=True
USER=False

engine = create_async_engine(settings.DATABASE_URL)
db_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    email = Column(String, nullable=False, unique=True, primary_key=True)
    role = Column(Boolean, nullable=False, default=USER)
    name = Column(String, default='')
    phone = Column(String, unique=True)
    address = Column(String, default='')
    
class UserInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def create_user(self, email: str, role: bool, name: str, phone: str, address: str) -> User:
        new_user = User(email=email, role=role, name=name, phone=phone, address=address)
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user
    
    async def get_user(self, email: str) -> User:
        user = await self.db_session.get(User, email)
        return user
    
    async def delete_user(self, email: str)->Boolean:
        user = await self.db_session.get(User, email)
        self.db_session.delete(user)
        await self.db_session.commit()
        return True
    
    async def update_user(self, email: str, name: Optional[str], phone: Optional[str], address: Optional[str])->User:
        user = await self.db_session.get(User, email)
        for attr, value in zip(["name", "phone", "address"], [name, phone, address]):
            if value is not None:
                setattr(user, attr, value)
        await self.db_session.commit()
        return user
    