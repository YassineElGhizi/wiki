from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import (Column, Integer, String, DateTime, Boolean, Text)
from sqlalchemy import create_engine
import datetime
import pathlib

DBSession = scoped_session(sessionmaker())
Base = declarative_base()
pwd = pathlib.Path(__file__).parent.resolve()
engine = create_engine(f"sqlite:////{pwd}/wiki.db", echo=False)
DBSession.configure(bind=engine)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    id_parent = Column(Integer, default=None)
    name = Column(String(50))
    translated_name = Column(String(255))
    link = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    id_parent = Column(Integer, default=None)
    title = Column(String(50))
    link = Column(String(50), nullable=True, unique=True)
    brief = Column(String(500))
    outro = Column(String(500))
    body = Column(Text)
    seo = Column(String(255))
    lang = Column(String(5))
    view_count = Column(Integer, default=0)
    search_count = Column(Integer, default=0)
    category_id = Column(Integer)
    image = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.now)


def migrate():
    Base.metadata.create_all(engine)


def add_column_image():
    engine.execute('alter table articles add column image String')


if __name__ == '__main__':
    migrate()
    add_column_image()
