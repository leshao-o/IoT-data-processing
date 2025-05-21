from app.CRUD.base import BaseCRUD
from app.models import UserORM
from app.schemas import User


class UserCRUD(BaseCRUD):
    model = UserORM
    schema = User
