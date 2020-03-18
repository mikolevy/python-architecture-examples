from sqlalchemy import Table, Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import mapper, relationship

from fexample.db import metadata
from fexample.loans.domain_model import InsuranceStatus, Insurance, Pause

insurance = Table(
    'insurance', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('identifier', String(255)),
    Column('car_id', String(255)),
    Column('protection_end', DateTime),
    Column('status', Enum(InsuranceStatus)),
)

pause = Table(
    'pause', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('begin_at', DateTime),
    Column('end_at', DateTime),
    Column('insurance_identifier', ForeignKey('insurance.identifier')),
)


def run_mappers():
    mapper(Insurance, insurance, properties={
        'pauses': relationship(Pause, backref='insurance', order_by=pause.c.begin_at),
    })
    mapper(Pause, pause)


