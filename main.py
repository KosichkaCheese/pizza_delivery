# import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
# import settings
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
from users import user_router
from admin import admin_router
# engine = create_async_engine(settings.DATABASE_URL)
# session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI(title='Pizza API', version='0.0.1')

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(admin_router)

app.include_router(main_router)

