import pytest
from unittest.mock import AsyncMock, MagicMock
from main_service import admin_service
from api.models import Pizza, Pizzaedit
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


class TestCreatePizzaService:
    @pytest.mark.asyncio
    async def test_create_pizza_success(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.create_pizza = AsyncMock(return_value=SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        ))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza = Pizza(name="Test Pizza", cost=10, description="Tasty pizza",
                      image="link", available=True)
        result = await admin_service.create_pizza_service(pizza)

        assert result["status"] == 200
        assert result["data"] == SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        )
        pizza_int.create_pizza.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_pizza_error(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.create_pizza = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza = Pizza(name="Test Pizza", cost=10, description="Tasty pizza",
                      image="link", available=True)
        result = await admin_service.create_pizza_service(pizza)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        pizza_int.create_pizza.assert_called_once()


class TestDeletePizzaService:
    @pytest.mark.asyncio
    async def test_delete_pizza_success(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.delete_pizza = AsyncMock(return_value=True)
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        result = await admin_service.delete_pizza_service(pizza_id)

        assert result["status"] == 200
        assert result["message"] == "Pizza deleted successfully"
        pizza_int.delete_pizza.assert_called_once_with(id=pizza_id)

    @pytest.mark.asyncio
    async def test_delete_pizza_error(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.delete_pizza = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        result = await admin_service.delete_pizza_service(pizza_id)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        pizza_int.delete_pizza.assert_called_once_with(id=pizza_id)


class TestGetPizzaService:
    @pytest.mark.asyncio
    async def test_get_pizza_success(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.get_pizza = AsyncMock(return_value=SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        ))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        result = await admin_service.get_pizza_service(pizza_id)

        assert result["status"] == 200
        assert result["data"] == SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        )
        pizza_int.get_pizza.assert_called_once_with(id=pizza_id)

    @pytest.mark.asyncio
    async def test_get_pizza_error(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.get_pizza = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        result = await admin_service.get_pizza_service(pizza_id)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        pizza_int.get_pizza.assert_called_once_with(id=pizza_id)


class TestGetPizzaListService:
    @pytest.mark.asyncio
    async def test_get_pizza_list_success(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.get_pizza_list = AsyncMock(return_value=[SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        ),
            SimpleNamespace(
            id="pizza_id2",
            name="Test Pizza2",
            cost=10,
            description=None,
            image=None,
            available=True
        )])
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        result = await admin_service.get_pizza_list_service()

        assert result["status"] == 200
        assert result["data"] == [SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        ),
            SimpleNamespace(
            id="pizza_id2",
            name="Test Pizza2",
            cost=10,
            description=None,
            image=None,
            available=True
        )]
        pizza_int.get_pizza_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_pizza_list_error(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.get_pizza_list = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        result = await admin_service.get_pizza_list_service()

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        pizza_int.get_pizza_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_pizza_list_empty(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.get_pizza_list = AsyncMock(
            return_value=[])
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        result = await admin_service.get_pizza_list_service()

        assert result["status"] == 200
        assert result["data"] == []
        pizza_int.get_pizza_list.assert_called_once()


class TestUpdatePizzaService:
    @pytest.mark.asyncio
    async def test_update_pizza_success(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.update_pizza = AsyncMock(return_value=SimpleNamespace(
            id="pizza_id",
            name="Test",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        ))
        pizza_int.get_pizza = AsyncMock(return_value=SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description=None,
            image="link",
            available=True
        ))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        pizza_data = Pizzaedit(
            name="Test",
            description="Tasty pizza"
        )
        result = await admin_service.update_pizza_service(pizza_id, pizza_data=pizza_data)

        assert result["status"] == 200
        assert result["data"] == SimpleNamespace(
            id="pizza_id",
            name="Test",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=True
        )
        pizza_int.update_pizza.assert_called_once_with(
            id=pizza_id, available=None, name="Test", cost=None, description="Tasty pizza", image=None)

    @pytest.mark.asyncio
    async def test_update_pizza_error(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.update_pizza = AsyncMock(
            side_effect=Exception("Database error"))
        pizza_int.get_pizza = AsyncMock(return_value=SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description=None,
            image="link",
            available=True
        ))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        pizza_data = Pizzaedit(
            name="Test",
            description="Tasty pizza"
        )
        result = await admin_service.update_pizza_service(pizza_id, pizza_data=pizza_data)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        pizza_int.update_pizza.assert_called_once_with(
            id=pizza_id, available=None, name="Test", cost=None, description="Tasty pizza", image=None)

    @pytest.mark.asyncio
    async def test_update_pizza_not_found(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.get_pizza = AsyncMock(return_value=None)
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        pizza_data = Pizzaedit(
            name="Test",
            description="Tasty pizza"
        )
        result = await admin_service.update_pizza_service(pizza_id, pizza_data=pizza_data)

        assert result["status"] == 404
        assert result["message"] == "Pizza not found"
        pizza_int.get_pizza.assert_called_once_with(id=pizza_id)


class TestOrderListService:
    @pytest.mark.asyncio
    async def test_get_order_list_success(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_order_list = AsyncMock(return_value=[SimpleNamespace(
            id="order_id",
            status=1,
            total_cost=10,
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            address="123 Test St",
            phone="123"
        )])
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        result = await admin_service.get_order_list_service()

        assert result["status"] == 200
        assert result["data"] == [SimpleNamespace(
            id="order_id",
            status=1,
            total_cost=10,
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            address="123 Test St",
            phone="123"
        )]
        order_int.get_order_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_order_list_empty(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_order_list = AsyncMock(
            return_value=[])
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        result = await admin_service.get_order_list_service()

        assert result["status"] == 200
        assert result["data"] == []
        order_int.get_order_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_order_list_error(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_order_list = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        result = await admin_service.get_order_list_service()

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        order_int.get_order_list.assert_called_once()


class TestGetOrdersByStatusService:
    @pytest.mark.asyncio
    async def test_get_orders_by_status_success(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_orders_by_status = AsyncMock(return_value=[SimpleNamespace(
            id="order_id",
            status=1,
            total_cost=10,
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            address="123 Test St",
            phone="123"
        )])
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        status = 1
        result = await admin_service.get_orders_by_status_service(status)

        assert result["status"] == 200
        assert result["data"] == [SimpleNamespace(
            id="order_id",
            status=1,
            total_cost=10,
            user_email="test@example.com",
            time="2023-01-01T00:00:00",
            address="123 Test St",
            phone="123")]
        order_int.get_orders_by_status.assert_called_once_with(status=status)

    @pytest.mark.asyncio
    async def test_get_orders_by_status_error(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.get_orders_by_status = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        status = 1
        result = await admin_service.get_orders_by_status_service(status)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        order_int.get_orders_by_status.assert_called_once_with(status=status)


class TestGetOrderContentService:
    @pytest.mark.asyncio
    async def test_get_order_content_success(self, mocker, db_session_mock):
        order_content_int = AsyncMock()
        order_content_int.get_order_content = AsyncMock(return_value=[{
            "pizza_id": "pizza_id",
            "pizza_name": "Test Pizza",
            "pizza_cost": 10,
            "count": 1},
            {
                "pizza_id": "pizza_id2",
                "pizza_name": "Test Pizza 2",
                "pizza_cost": 20,
                "count": 2
        }])
        mocker.patch('services.admin_service.OrderContentInteract',
                     return_value=order_content_int)

        order_id = "order_id"
        result = await admin_service.get_order_content_service(order_id)

        assert result["status"] == 200
        assert result["data"] == [{
            "pizza_id": "pizza_id",
            "pizza_name": "Test Pizza",
            "pizza_cost": 10,
            "count": 1},
            {
                "pizza_id": "pizza_id2",
                "pizza_name": "Test Pizza 2",
                "pizza_cost": 20,
                "count": 2
        }]
        order_content_int.get_order_content.assert_called_once_with(
            order_id=order_id)

    @pytest.mark.asyncio
    async def test_get_order_content_error(self, mocker, db_session_mock):
        order_content_int = AsyncMock()
        order_content_int.get_order_content = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.OrderContentInteract',
                     return_value=order_content_int)

        order_id = "order_id"
        result = await admin_service.get_order_content_service(order_id)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        order_content_int.get_order_content.assert_called_once_with(
            order_id=order_id)


class TestUpdateOrderStatusService:
    @pytest.mark.asyncio
    async def test_update_order_status_success(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.update_order_status = AsyncMock(return_value=True)
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        order_id = "order_id"
        status = 2
        result = await admin_service.update_order_status_service(
            order_id, status)

        assert result["status"] == 200
        assert result["message"] == "Order status updated successfully"
        order_int.update_order_status.assert_called_once_with(
            id=order_id, status=status)

    @pytest.mark.asyncio
    async def test_update_order_status_error(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.update_order_status = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        order_id = "order_id"
        status = 2
        result = await admin_service.update_order_status_service(
            order_id, status)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        order_int.update_order_status.assert_called_once_with(
            id=order_id, status=status)

    @pytest.mark.asyncio
    async def test_update_order_status_invalid_status(self, mocker, db_session_mock):
        order_int = AsyncMock()
        order_int.update_order_status = AsyncMock(return_value=True)
        mocker.patch('services.admin_service.OrderInteract',
                     return_value=order_int)

        order_id = "order_id"
        status = 5
        result = await admin_service.update_order_status_service(
            order_id, status)

        assert result["status"] == 400
        assert result["message"] == "Invalid status"


class TestPizzaAnavailableService:
    @pytest.mark.asyncio
    async def test_pizza_available_success(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.update_pizza = AsyncMock(return_value=SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=False
        ))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        result = await admin_service.pizza_unavailable_service(pizza_id)

        assert result["status"] == 200
        assert result["data"] == SimpleNamespace(
            id="pizza_id",
            name="Test Pizza",
            cost=10,
            description="Tasty pizza",
            image="link",
            available=False
        )
        pizza_int.update_pizza.assert_called_once_with(
            id=pizza_id, available=False, name=None, cost=None, description=None, image=None
        )

    @pytest.mark.asyncio
    async def test_pizza_available_error(self, mocker, db_session_mock):
        pizza_int = AsyncMock()
        pizza_int.update_pizza = AsyncMock(
            side_effect=Exception("Database error"))
        mocker.patch('services.admin_service.PizzaInteract',
                     return_value=pizza_int)

        pizza_id = "pizza_id"
        result = await admin_service.pizza_unavailable_service(pizza_id)

        assert result["status"] == 500
        assert result["message"] == "Internal server error"
        pizza_int.update_pizza.assert_called_once_with(
            id=pizza_id, available=False, name=None, cost=None, description=None, image=None)
