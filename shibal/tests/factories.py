from datetime import datetime, timedelta
from uuid import uuid4

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models.operations import OperationTypes
from app.models.orders import Order, OrderTypes
from app.models.users import User


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        # FIXME: fix async factory creation
        # sqlalchemy_session_factory = async_session
        # sqlalchemy_session_persistence = "flush"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    chat_id = factory.Faker("pyint", min_value=1, max_value=1_000_000)
    op_balance = 324
    created = datetime.now()


class OrderFactory(BaseFactory):
    class Meta:
        model = Order

    id = factory.LazyFunction(uuid4)
    user = factory.SubFactory(UserFactory)
    order_type = OrderTypes.START
    op_added = 324
    created = datetime.now()
    payed = datetime.now()


class OperationFactory(BaseFactory):
    class Meta:
        model = Order

    id = factory.LazyFunction(uuid4)
    user = factory.SubFactory(UserFactory)
    op_type = OperationTypes.TRIM
    details = factory.Dict({"length": 3000, "new_length": 1000})
    started = datetime.now() - timedelta(days=1)
    took = factory.Faker("pyfloat", min_value=0.1, max_value=100)
