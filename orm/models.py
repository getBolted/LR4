# coding: utf-8

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Depo(Base):
    __tablename__ = 'depos'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text)
    open_date = Column(Date)

    lines = relationship('Line', secondary='depos_to_lines')
    trains = relationship('Train', secondary='depos_to_trains')


class Line(Base):
    __tablename__ = 'lines'

    id = Column(Integer, primary_key=True, unique=True)
    color = Column(Text)
    name = Column(Text)
    year_open = Column(Integer)
    year_lst_st_open = Column(Integer)
    length = Column(Float)
    time_to_travel = Column(Integer)
    avg_depth = Column(Integer)
    avg_pasng_per_day = Column(Integer)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Train(Base):
    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text)
    expl_start = Column(Integer)
    expl_end = Column(Integer)
    max_speed = Column(Integer)
    voltage = Column(Integer)
    capacity = Column(Integer)


t_depos_to_lines = Table(
    'depos_to_lines', metadata,
    Column('depo_id', ForeignKey('depos.id')),
    Column('line_id', ForeignKey('lines.id'))
)


t_depos_to_trains = Table(
    'depos_to_trains', metadata,
    Column('depo_id', ForeignKey('depos.id'), nullable=False),
    Column('train_id', ForeignKey('trains.id'), nullable=False)
)


class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text)
    open_date = Column(Date)
    depth = Column(Float)
    station_type = Column(Text)
    line_id = Column(ForeignKey('lines.id'))

    line = relationship('Line')
