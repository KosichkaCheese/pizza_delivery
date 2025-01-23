from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Boolean
from db.db import User, Auth


class UserInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, email: str, role: bool, name: str, phone: str, address: str) -> User:
        new_user = User(email=email, role=role, name=name,
                        phone=phone, address=address)
        self.db_session.add(new_user)
        return new_user

    async def get_user(self, email: str) -> User:
        user = await self.db_session.get(User, email)
        return user

    async def delete_user(self, email: str) -> Boolean:
        user = await self.db_session.get(User, email)
        user_auth = await self.db_session.get(Auth, email)
        await self.db_session.delete(user_auth)
        await self.db_session.delete(user)
        await self.db_session.commit()
        return True

    async def update_user(self, email: str, name: Optional[str], phone: Optional[str], address: Optional[str]) -> User:
        user = await self.db_session.get(User, email)
        for attr, value in zip(["name", "phone", "address"], [name, phone, address]):
            if value is not None:
                setattr(user, attr, value)
        return user


class AuthInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_auth(self, email: str, password: str) -> Boolean:
        auth = Auth(email=email, password=password)
        self.db_session.add(auth)
        return True

    async def check_auth(self, email: str, password: str) -> Boolean:
        auth = await self.db_session.get(Auth, email)
        if auth.password == password:
            return True
        return False
