from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50),nullable=False)
    sur_name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=True)
    telephone = Column(String(12), nullable=True)
    email = Column(String(50), nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, " \
               f"sur_name={self.sur_name!r},father_name={self.father_name!r}, " \
               f"telephone={self.telephone!r}, email={self.email!r})"







engine = create_engine('sqlite:///dataspace.db')
Base.metadata.create_all(engine)











