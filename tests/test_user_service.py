import pytest
from unittest.mock import AsyncMock, MagicMock
from services import user_service
from api.models import Usercreate, Useredit
from types import SimpleNamespace


@pytest.fixture
def db_session_mock(mocker):
    # Мокаем db_session, чтобы исключить реальную базу данных
    session_mock = AsyncMock()
    session_enter_mock = AsyncMock(return_value=session_mock)
    session_context_manager = MagicMock(
        __aenter__=session_enter_mock, __aexit__=AsyncMock())
    mocker.patch("db.db.db_session", return_value=session_context_manager)
    return session_mock


class TestCreateUserService:
    @pytest.mark.asyncio
    async def test_create_user_success(self, mocker, db_session_mock):
        # Создаем моки для классов UserInteract и AuthInteract
        user_data_mock = AsyncMock()
        auth_mock = AsyncMock()

        # Настраиваем возвращаемые значения моков при вызове методов
        user_data_mock.create_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        })
        auth_mock.create_auth = AsyncMock(return_value=True)

        # Подменяем классы UserInteract и AuthInteract внутри модуля user_service
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)
        mocker.patch('services.user_service.AuthInteract',
                     return_value=auth_mock)

        # Создаем тестовые данные
        test_user = Usercreate(
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        )
        password = "securepassword"

        # Вызываем тестируемую функцию
        result = await user_service.create_user_service(test_user, password)

        # Проверяем, что моки были вызваны с нужными аргументами
        user_data_mock.create_user.assert_awaited_once_with(
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        )
        auth_mock.create_auth.assert_awaited_once_with(
            email="test@example.com", password=password)

        # Проверяем результат выполнения функции
        assert result["status"] == 200
        assert "data" in result
        assert result["data"] == {
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        }

    @pytest.mark.asyncio
    async def test_create_user_error(self, mocker, db_session_mock):
        # Создаем моки для классов UserInteract и AuthInteract
        user_data_mock = AsyncMock()
        auth_mock = AsyncMock()

        # Настраиваем возвращаемые значения моков при вызове методов
        user_data_mock.create_user = AsyncMock(
            side_effect=Exception("Database error"))
        auth_mock.create_auth = AsyncMock(return_value=True)

        # Подменяем классы UserInteract и AuthInteract внутри модуля user_service
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)
        mocker.patch('services.user_service.AuthInteract',
                     return_value=auth_mock)

        # Создаем тестовые данные
        test_user = Usercreate(
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        )
        password = "securepassword"

        # Вызываем тестируемую функцию
        result = await user_service.create_user_service(test_user, password)

        # Проверяем результат выполнения функции
        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        user_data_mock.create_user.assert_awaited_once_with(
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        )

    @pytest.mark.asyncio
    async def test_create_auth_error(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        auth_mock = AsyncMock()

        # Настраиваем create_auth для выбрасывания исключения
        user_data_mock.create_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        })
        auth_mock.create_auth = AsyncMock(side_effect=Exception("Auth error"))

        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)
        mocker.patch('services.user_service.AuthInteract',
                     return_value=auth_mock)

        test_user = Usercreate(
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        )
        password = "securepassword"

        result = await user_service.create_user_service(test_user, password)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"


class TestGetUserService:
    @pytest.mark.asyncio
    async def test_get_user_success(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.get_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        })
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        email = "test@example.com"
        result = await user_service.get_user_service(email)

        assert result["status"] == 200
        assert result["data"] == {
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        }
        user_data_mock.get_user.assert_called_once_with(email=email)

    @pytest.mark.asyncio
    async def test_get_user_error(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.get_user = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        email = "test@example.com"
        result = await user_service.get_user_service(email)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        user_data_mock.get_user.assert_called_once_with(email=email)

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.get_user = AsyncMock(return_value=None)
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        email = "test@example.com"
        result = await user_service.get_user_service(email)

        assert result["status"] == 404
        assert result["message"] == "User not found"
        user_data_mock.get_user.assert_called_once_with(email=email)


class TestDeleteUserService:
    @pytest.mark.asyncio
    async def test_delete_user_success(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.delete_user = AsyncMock(return_value=True)
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        email = "test@example.com"
        result = await user_service.delete_user_service(email)

        assert result["status"] == 200
        assert result["message"] == "User deleted successfully"
        user_data_mock.delete_user.assert_called_once_with(email=email)

    @pytest.mark.asyncio
    async def test_delete_user_exc(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.delete_user = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        email = "test@example.com"
        result = await user_service.delete_user_service(email)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        user_data_mock.delete_user.assert_called_once_with(email=email)

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.get_user = AsyncMock(return_value=False)
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        email = "test@example.com"
        result = await user_service.delete_user_service(email)

        assert result["status"] == 404
        assert result["message"] == "User not found"


class TestUpdateUserService:
    @pytest.mark.asyncio
    async def test_update_user_success(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.update_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test",
            "phone": "123",
            "address": "123 Test St"
        })
        user_data_mock.get_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        })
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        user = Useredit(
            email="test@example.com",
            name="Test",
            phone="123",
            address="123 Test St")
        result = await user_service.update_user_service(user)

        assert result["status"] == 200
        assert result["data"] == {
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test",
            "phone": "123",
            "address": "123 Test St"
        }
        user_data_mock.update_user.assert_called_once_with(
            email="test@example.com",
            name="Test",
            phone="123",
            address="123 Test St"
        )

    @pytest.mark.asyncio
    async def test_update_user_part(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.update_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test",
            "phone": "123",
            "address": "123 Test St"
        })
        user_data_mock.get_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        })
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        user = Useredit(
            email="test@example.com",
            name="Test")
        result = await user_service.update_user_service(user)

        assert result["status"] == 200
        assert result["data"] == {
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test",
            "phone": "123",
            "address": "123 Test St"
        }
        user_data_mock.update_user.assert_called_once_with(
            email="test@example.com",
            name="Test",
            phone=None,
            address=None
        )

    @pytest.mark.asyncio
    async def test_update_user_error(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.update_user = AsyncMock(
            side_effect=Exception("Database error"))
        user_data_mock.get_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        })
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        user = Useredit(email="test@example.com", name="Test")
        result = await user_service.update_user_service(user)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        user_data_mock.update_user.assert_called_once_with(
            email="test@example.com",
            name="Test",
            phone=None,
            address=None
        )

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, mocker, db_session_mock):
        user_data_mock = AsyncMock()
        user_data_mock.get_user = AsyncMock(return_value=None)
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_data_mock)

        user = Useredit(email="test@example.com", name="Test")
        result = await user_service.update_user_service(user)

        assert result["status"] == 404
        assert result["message"] == "User not found"


class TestCheckAuthService:
    @pytest.mark.asyncio
    async def test_check_auth_success(self, mocker, db_session_mock):
        auth_data_mock = AsyncMock()
        auth_data_mock.check_auth = AsyncMock(return_value=True)
        mocker.patch('services.user_service.AuthInteract',
                     return_value=auth_data_mock)

        email = "test@example.com"
        password = "securepassword"
        result = await user_service.check_auth_service(email, password)

        assert result["status"] == 200
        assert result["message"] == "Authentication successful"
        auth_data_mock.check_auth.assert_called_once_with(
            email=email, password=password)

    @pytest.mark.asyncio
    async def test_check_auth_fail(self, mocker, db_session_mock):
        auth_data_mock = AsyncMock()
        auth_data_mock.check_auth = AsyncMock(return_value=False)
        mocker.patch('services.user_service.AuthInteract',
                     return_value=auth_data_mock)

        email = "test@example.com"
        password = "wrongpassword"
        result = await user_service.check_auth_service(email, password)

        assert result["status"] == 401
        assert result["message"] == "Authentication failed"
        auth_data_mock.check_auth.assert_called_once_with(
            email=email, password=password)

    @pytest.mark.asyncio
    async def test_check_auth_error(self, mocker, db_session_mock):
        auth_data_mock = AsyncMock()
        auth_data_mock.check_auth = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.user_service.AuthInteract',
                     return_value=auth_data_mock)

        email = "test@example.com"
        password = "securepassword"
        result = await user_service.check_auth_service(email, password)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        auth_data_mock.check_auth.assert_called_once_with(
            email=email, password=password)


class TestAddToCartService:
    @pytest.mark.asyncio
    async def test_add_to_cart_success(self, mocker, db_session_mock):
        user_int = AsyncMock()
        user_int.get_user = AsyncMock(return_value={
            "id": "user_id",
            "email": "test@example.com",
            "role": True,
            "name": "Test User",
            "phone": "123",
            "address": "123 Test St"
        })
        pizza_int = AsyncMock()
        pizza_int.get_pizza = AsyncMock(return_value={
            "id": "pizza_id",
            "name": "Test Pizza",
            "cost": 10,
            "description": "Tasty pizza",
            "image": "link",
            "available": True
        })
        order_int = AsyncMock()
        order_int.current_order = AsyncMock(return_value=SimpleNamespace(
            id="order_id",
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            summ=10,
            address="123 Test St",
            phone="123",
            status=0))
        order_content_int = AsyncMock()
        order_content_int.add_order_content = AsyncMock(return_value={
            "id": "order_content_id",
            "order_id": "order_id",
            "pizza_id": "pizza_id",
            "count": 1
        })
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_int)
        mocker.patch('services.user_service.PizzaInteract',
                     return_value=pizza_int)
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)
        mocker.patch('services.user_service.OrderContentInteract',
                     return_value=order_content_int)

        email = "test@example.com"
        pizza_id = "pizza_id"
        count = 1
        result = await user_service.add_to_cart_service(email, pizza_id, count)

        assert result["status"] == 200
        assert result["message"] == "Pizza added to cart"
        order_content_int.add_order_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_to_cart_neworder(self, mocker, db_session_mock):
        user_int = AsyncMock()
        user_int.get_user = AsyncMock(return_value=SimpleNamespace(
            id="user_id",
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        ))
        pizza_int = AsyncMock()
        pizza_int.get_pizza = AsyncMock(return_value=SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        ))
        order_int = AsyncMock()
        order_int.current_order = AsyncMock(side_effect=[None, SimpleNamespace(
            id="order_id",
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            summ=10,
            address="123 Test St",
            phone="123",
            status=0)])
        order_int.create_order = AsyncMock(return_value={
            "id": "order_id",
            "user_email": "test@example.com",
            "time": "2023-01-01T00:00:00",
            "summ": 10,
            "address": "123 Test St",
            "phone": "123",
            "status": 0
        })
        order_content_int = AsyncMock()
        order_content_int.add_order_content = AsyncMock(return_value={
            "id": "order_content_id",
            "order_id": "order_id",
            "pizza_id": "pizza_id",
            "count": 1
        })
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_int)
        mocker.patch('services.user_service.PizzaInteract',
                     return_value=pizza_int)
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)
        mocker.patch('services.user_service.OrderContentInteract',
                     return_value=order_content_int)

        email = "test@example.com"
        pizza_id = "pizza_id"
        count = 1
        result = await user_service.add_to_cart_service(email, pizza_id, count)

        assert result["status"] == 200
        assert result["message"] == "Pizza added to cart"
        order_int.create_order.assert_called_once()
        order_content_int.add_order_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_to_cart_error(self, mocker, db_session_mock):
        user_int = AsyncMock()
        user_int.get_user = AsyncMock(return_value=SimpleNamespace(
            id="user_id",
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        ))
        pizza_int = AsyncMock()
        pizza_int.get_pizza = AsyncMock(return_value={
            "id": "pizza_id",
            "name": "Test Pizza",
            "cost": 10,
            "description": "Tasty pizza",
            "image": "link",
            "available": True
        })
        order_int = AsyncMock()
        order_int.current_order = AsyncMock(return_value=SimpleNamespace(
            id="order_id",
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            summ=10,
            address="123 Test St",
            phone="123",
            status=0
        ))
        order_content_int = AsyncMock()
        order_content_int.add_order_content = AsyncMock(
            side_effect=Exception("Error adding to cart"))
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_int)
        mocker.patch('services.user_service.PizzaInteract',
                     return_value=pizza_int)
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)
        mocker.patch('services.user_service.OrderContentInteract',
                     return_value=order_content_int)

        email = "test@example.com"
        pizza_id = "pizza_id"
        count = 1
        result = await user_service.add_to_cart_service(email, pizza_id, count)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        order_content_int.add_order_content.assert_called_once()


class TestGetUserOrdersService:
    @pytest.mark.asyncio
    async def test_get_user_orders_success(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_user_orders = AsyncMock(return_value=[
            {
                "id": "order_id",
                "user_email": "test@example.com",
                "time": "2023-01-01T00:00:00",
                "summ": 10,
                "address": "123 Test St",
                "phone": "123",
                "status": 0
            },
            {
                "id": "order_id2",
                "user_email": "test@example.com",
                "time": "2023-01-01T00:00:00",
                "summ": 10,
                "address": "123 Test St",
                "phone": "123",
                "status": 1
            }
        ])
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)

        email = "test@example.com"
        result = await user_service.get_user_orders_service(email)

        assert result["status"] == 200
        assert result["data"] == [
            {
                "id": "order_id",
                "user_email": "test@example.com",
                "time": "2023-01-01T00:00:00",
                "summ": 10,
                "address": "123 Test St",
                "phone": "123",
                "status": 0
            },
            {
                "id": "order_id2",
                "user_email": "test@example.com",
                "time": "2023-01-01T00:00:00",
                "summ": 10,
                "address": "123 Test St",
                "phone": "123",
                "status": 1
            }]
        order_int.get_user_orders.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_get_user_orders_error(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_user_orders = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)

        email = "test@example.com"
        result = await user_service.get_user_orders_service(email)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        order_int.get_user_orders.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_get_user_orders_empty(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_user_orders = AsyncMock(return_value=[])
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)

        email = "test@example.com"
        result = await user_service.get_user_orders_service(email)

        assert result["status"] == 200
        assert result["data"] == []
        order_int.get_user_orders.assert_called_once_with(email)


class TestPlaceOrderService:
    @pytest.mark.asyncio
    async def test_place_order_success(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.place_order = AsyncMock(return_value={
            "id": "order_id",
            "user_email": "test@example.com",
            "time": "2023-01-01T00:00:00",
            "summ": 10,
            "address": "123 Test St",
            "phone": "123",
            "status": 1
        })
        order_int.current_order = AsyncMock(return_value=SimpleNamespace(
            id="order_id",
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            summ=10,
            address="123 Test St",
            phone="123",
            status=0))
        order_content_int = AsyncMock()
        order_content_int.get_order_content = AsyncMock(return_value=[
            {
                "pizza_id": "pizza_id",
                "pizza_name": "Test Pizza",
                "pizza_cost": 10,
                "count": 1
            }
        ])
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)
        mocker.patch('services.user_service.OrderContentInteract',
                     return_value=order_content_int)

        email = "test@example.com"
        result = await user_service.place_order_service(email, "123 Test St", "123")

        assert result["status"] == 200
        assert result["data"] == {
            "id": "order_id",
            "user_email": "test@example.com",
            "time": "2023-01-01T00:00:00",
            "summ": 10,
            "address": "123 Test St",
            "phone": "123",
            "status": 1
        }
        order_int.place_order.assert_called_once()

    @pytest.mark.asyncio
    async def test_place_order_no_params(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.place_order = AsyncMock(return_value={
            "id": "order_id",
            "user_email": "test@example.com",
            "time": "2023-01-01T00:00:00",
            "summ": 10,
            "address": "123 Test St",
            "phone": "123",
            "status": 1
        })
        order_int.current_order = AsyncMock(return_value=SimpleNamespace(
            id="order_id",
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            summ=10,
            address="123 Test St",
            phone="123",
            status=0))
        order_content_int = AsyncMock()
        order_content_int.get_order_content = AsyncMock(return_value=[
            {
                "pizza_id": "pizza_id",
                "pizza_name": "Test Pizza",
                "pizza_cost": 10,
                "count": 1
            }
        ])
        user_int = AsyncMock()
        user_int.get_user = AsyncMock(return_value=SimpleNamespace(
            id="user_id",
            email="test@example.com",
            role=True,
            name="Test User",
            phone="123",
            address="123 Test St"
        ))
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)
        mocker.patch('services.user_service.OrderContentInteract',
                     return_value=order_content_int)
        mocker.patch('services.user_service.UserInteract',
                     return_value=user_int)

        email = "test@example.com"
        result = await user_service.place_order_service(email)

        assert result["status"] == 200
        assert result["data"] == {
            "id": "order_id",
            "user_email": "test@example.com",
            "time": "2023-01-01T00:00:00",
            "summ": 10,
            "address": "123 Test St",
            "phone": "123",
            "status": 1
        }
        order_int.place_order.assert_called_once()
        user_int.get_user.assert_called_once_with(email=email)

    @pytest.mark.asyncio
    async def test_place_order_empty_cart(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.current_order = AsyncMock(return_value=None)
        mocker.patch('services.user_service.OrderInteract',
                     return_value=order_int)

        email = "test@example.com"
        result = await user_service.place_order_service(email)

        assert result["status"] == 404
        assert result["message"] == "cart is empty"
