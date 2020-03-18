from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

from fexample import config

engine = create_engine(config.DB_URI, convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def init_db():
    from fexample.insurance import orm_model
    orm_model.run_mappers()
    metadata.create_all(bind=engine)


def drop_tables():
    metadata.drop_all(bind=engine)
