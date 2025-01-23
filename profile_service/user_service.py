from api.models import Usercreate, Useredit
from db.db import db_session
from db.db_repository import AuthInteract, UserInteract


async def create_user_service(user: Usercreate, password: str):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            auth = AuthInteract(session)
            try:
                new_user = await user_data.create_user(
                    email=user.email,
                    role=user.role,
                    name=user.name,
                    phone=user.phone,
                    address=user.address
                )
                new_auth = await auth.create_auth(email=user.email, password=password)
                if new_auth:
                    print(password)
            except Exception as e:
                print("error while creating user:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": new_user}


async def get_user_service(email: str):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            try:
                user = await user_data.get_user(email=email)
            except Exception as e:
                print("error while getting user:", e)
                return {"status": 500, "message": "Internal server error"}
            if user:
                return {"status": 200, "data": user}
            else:
                return {"status": 404, "message": "User not found"}


async def delete_user_service(email: str):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            try:
                user = await user_data.get_user(email=email)
                if user:
                    res = await user_data.delete_user(email=email)
                else:
                    return {"status": 404, "message": "User not found"}
            except Exception as e:
                print("error while deleting user:", e)
                return {"status": 500, "message": "Internal server error"}
            if res:
                return {"status": 200, "message": "User deleted successfully"}
            else:
                return {"status": 500, "message": "Internal server error"}


async def update_user_service(user: Useredit):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            try:
                cur_user = await user_data.get_user(email=user.email)
                if not cur_user:
                    return {"status": 404, "message": "User not found"}

                updated_user = await user_data.update_user(
                    email=user.email,
                    name=user.name,
                    phone=user.phone,
                    address=user.address
                )
            except Exception as e:
                print("error while updating user:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": updated_user}


async def check_auth_service(email: str, password: str):
    async with db_session() as session:
        async with session.begin():
            auth = AuthInteract(session)
            try:
                auth_result = await auth.check_auth(email=email, password=password)
            except Exception as e:
                print("error while checking auth:", e)
                return {"status": 500, "message": "Internal server error"}
            if auth_result:
                return {"status": 200, "message": "Authentication successful"}
            else:
                return {"status": 401, "message": "Authentication failed"}
