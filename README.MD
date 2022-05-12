# Лабораторная работа #4 - Работа с реляционной базой данных на примере SQLite

В рамках данной ЛР мы спроектируем и реализуем базу данных станций Московского метрополитена 
в СУБД SQLite, используя библиотеку SQLAlchemy для манипуляции данными.

Справку по работе с SQLAlchemy можно найти [здесь](https://ru.wikibooks.org/wiki/SQLAlchemy)

Для работы нам понадобится установить 2 сторниих пакета:

```
pip install sqlacodegen sqlalchemy
```

### Создание БД ручным способом

* Для создания таблиц с данными необходимо задать атрибуты, primary key, а также constraint`ы и foreign keys 
при необходимости: 


```
CREATE TABLE stations (
    id           integer not null
        constraint stations_pk
            primary key,
    name         text,
    open_date    date,
    depth        real,
    station_type text,
    line_id      integer
        references lines
);
```

* Для создания промежуточных таблиц необходимо задать 2 поля с id кортежей соединяемых таблиц:

```
CREATE TABLE depos_to_trains
(
    depo_id  INTEGER not null
        references depos,
    train_id INTEGER not null
        references trains
);
```


### Создание БД из моделей SQLAlchemy

В SQLAlchemy таблица представляется классом, атрибуты которого соответствуют колонкам таблицы
```
class Depo(Base):
    __tablename__ = 'depos'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    open_date = Column(Date)

    lines = relationship('Line', secondary='depos_to_lines')
    trains = relationship('Train', secondary='depos_to_trains')
```

Параметр secondary ссылается на объект Table, который необходимо описать отдельно для создания промежуточной таблицы
```
t_depos_to_trains = Table(
    'depos_to_trains', metadata,
    Column('depo_id', ForeignKey('depos.id'), nullable=False),
    Column('train_id', ForeignKey('trains.id'), nullable=False)
)
```

После описания всех таблиц и реляций необходимо создать объекты engine и metadata:
```
Base = declarative_base()
metadata = Base.metadata
...
engine = db.create_engine('sqlite:///dbname.db', echo=True)
```

Вызов метода `create_all` создаст БД в соответсвии со схемой из реляционной модели:
```
metadata.create_all(engine)
```

### Создание моделей SQLAlchemy по схеме БД

Обратная операция также имеет место быть и иногда бывает очень к месту. Для автоматизированной генерации моделей 
воспользуемся командой:

```
sqlacodegen sqlite:///dbname.db --outfile .\orm\models.py
```
где параметр `--outfile` отвечает за расположение итогового файла с моделями таблиц БД 

### Запросы 

Запросы пишутся в рамках синтакисиса SQLAlchemy, примеры представлены в query_db.py