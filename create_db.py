import sqlalchemy as db
from orm.models import metadata

if __name__ == '__main__':
    # Создаем БД из моделей таблиц
    engine = db.create_engine('sqlite:///metro_cr.db', echo=True)
    metadata.create_all(engine)
