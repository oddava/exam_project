from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Model


class User(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String)
    surname: Mapped[String] = mapped_column(String)
    age: Mapped[Integer] = mapped_column(Integer)