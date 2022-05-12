from operator import and_

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from orm.models import *
from datetime import date


def add_station():
    new_station = Station(name='Реутов', open_date=date(2023, 8, 10), depth=0, station_type='наземная крытая',
                          line_id=8)
    session.add(new_station)
    session.commit()


def add_couple():
    stations = list()
    stations.append(
        Station(name='Реутов', open_date=date(2023, 8, 10), depth=0, station_type='наземная крытая', line_id=8))
    stations.append(
        Station(name='Никольская', open_date=date(2023, 10, 22), depth=0, station_type='наземная крытая', line_id=8))
    session.add_all(stations)
    session.commit()


def del_station():
    session.query(Station).filter(Station.name == 'Реутов').delete()
    session.commit()


def calc_mindept_by_type():
    query = db.select([
        Station.station_type.label('type'),
        db.func.min(Station.depth).label('min_depth')
    ]).where(Station.station_type.is_not(None)).group_by(Station.station_type).order_by('min_depth')
    result = engine.execute(query).fetchall()

    for rec in result:
        print(f'{rec}\n')


def calc_old_stations():
    """
    Выведем список не старше 1961 года, через которые курсировали вагоны серии А
    """
    query = db.select([Station.name]). \
        join(Line). \
        join(Depo, Line.depos). \
        join(Train, Depo.trains). \
        filter(and_(Train.name == 'А', db.func.date(Station.open_date) > '1961-01-01'))
    result = engine.execute(query).fetchall()

    for rec in result:
        print(f"{rec._mapping['name']}\n")


if __name__ == '__main__':
    engine = db.create_engine('sqlite:///metro.db', echo=True)
    Session = sessionmaker(bind=engine)  # Создаем класс Сессия, объекты которго будет создавать для исполнения запросов
    session = Session()

    # add_station(session)
    # add_couple(session)
    # del_station(session)
    # calc_mindept_by_type()
    calc_old_stations()

    session.close()
