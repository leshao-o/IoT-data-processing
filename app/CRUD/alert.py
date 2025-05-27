from app.CRUD.base import BaseCRUD
from app.models import AlertORM
from app.schemas.alert import Alert


class AlertCRUD(BaseCRUD):
    model = AlertORM
    schema = Alert
