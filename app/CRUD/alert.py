from app.CRUD.base import BaseCRUD
from app.models import AlertORM
from app.schemas import Alert


class AlertCRUD(BaseCRUD):
    model = AlertORM
    schema = Alert
