import sqlalchemy as db

if __name__ == '__main__':
    engine = db.create_engine('sqlite://metro.db')
    connection = engine.connect()