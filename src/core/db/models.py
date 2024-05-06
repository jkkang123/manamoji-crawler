from sqlalchemy import Column, VARCHAR, BINARY, TEXT, ForeignKey, Integer
from base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(BINARY(16), primary_key=True, index=True)
    name = Column(VARCHAR(100))


class Mangas(Base):
    __tablename__ = "mangas"

    id = Column(BINARY(16), primary_key=True, index=True)
    image = Column(VARCHAR(100))
    summary = Column(TEXT, nullable=False)
    content = Column(TEXT)


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(BINARY(16), primary_key=True, index=True)
    user_id = Column(BINARY(16), ForeignKey('users.id'))
    manga_id = Column(BINARY(16), ForeignKey('mangas.id'))
    content = Column(TEXT, nullable=False)
    score = Column(Integer)
