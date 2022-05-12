# Лабораторная работа #4 - Работа с реляционной базой данных на примере SQLite

В рамках данной ЛР мы спроектируем и реализуем базу данных станций Московского метрополитена 
в СУБД SQLite, используя библиотеку SQLAlchemy для манипуляции данными 

* Для создания таблиц с данными необходимо задать атрибуты, primary key, а также constraint`ы и foreign keys 
при необходимости: 

`CREATE TABLE stations (
    id           integer not null
        constraint stations_pk
            primary key autoincrement,
    name         text,
    open_date    date,
    depth        real,
    station_type text,
    line_id      integer, 
        references lines
);
create unique index stations_id_uindex
    on stations (id);
`

* Для создания промежуточных таблиц необходимо задать 2 поля с id кортежей соединяемых таблиц:

`CREATE TABLE depos_to_trains
(
    depo_id  INTEGER not null
        references depos,
    train_id INTEGER not null
        references trains
);`
