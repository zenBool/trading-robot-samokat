from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from db import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    foo_sample: Mapped[int]
    bar_sample: Mapped[int]

    # демонстация создания уникального ограничения таблицы из нескольких параметров
    __table_args__ = (UniqueConstraint("foo_sample", "bar_sample"),)
