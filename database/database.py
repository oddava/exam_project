from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update, func, \
    create_engine, select, BigInteger
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker, DeclarativeBase, selectinload, Mapped, mapped_column

from config import settings

# 🪓🪓
class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        __name = self.__name__[:1]
        for i in self.__name__[1:]:
            if i.isupper():
                __name += '_'
            __name += i
        __name = __name.lower()

        if __name.endswith('y'):
            __name = __name[:-1] + 'ie'
        return __name + 's'


class Database:
    def __init__(self):
        self._engine = None
        self._session = None

    def init(self):
        self._engine = create_engine(settings.postgresql_url)
        self._session = sessionmaker(self._engine, expire_on_commit=False)()
        db.create_all()

    def create_all(self):
        Base.metadata.create_all(self._engine)

    def drop_all(self):
        Base.metadata.drop_all(self._engine)

    def __getattr__(self, name):
        return getattr(self._session, name)


db = Database()
db.init()


class AbstractClass:
    @staticmethod
    def commit():
        try:
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    @classmethod
    def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)
        db.add(object_)
        cls.commit()
        return object_

    @classmethod
    def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        db.execute(query)
        cls.commit()

    @classmethod
    def get(cls, _id, *, relationship=None):
        query = select(cls).where(cls.id==_id)
        if relationship:
            query = query.options(selectinload(relationship))
        return (db.execute(query)).scalar()

    @classmethod
    def count(cls, criteria=None):
        query = select(func.count()).select_from(cls)
        if criteria is not None:
            query = query.where(criteria)

        return (db.execute(query)).scalar_one()

    @classmethod
    def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        db.execute(query)
        cls.commit()

    @classmethod
    def filter(cls, criteria, *, relationship=None, columns=None):
        if columns:
            query = select(*columns)
        else:
            query = select(cls)

        query = query.where(criteria)

        if relationship:
            query = query.options(selectinload(relationship))

        return db.execute(query).scalars().all()

    @classmethod
    def get_all(cls):
        return (db.execute(select(cls).order_by(cls.id.desc()))).scalars()


class Model(AbstractClass, Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    def __str__(self):
        return f"{self.id}"
