import json

from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry

db_host = '192.168.5.27'
db_port = 3306
db_user = 'parser'
db_password = '9ExtUS8uRyF9FSDf'
db_name = 'parser'

# Создаем движок SQLAlchemy (через SSH-туннель)
# Для этого используем локальный порт, который будет проброшен SSH-туннелем.
# Предположим, что туннель уже установлен и локальный порт — например, 3307.
import hashlib

local_port = 3307  # замените на ваш локальный порт


def string_to_md5(input_string):
    # Создаем объект MD5
    md5_obj = hashlib.md5()
    # Обновляем его байтовым представлением строки
    md5_obj.update(input_string.encode('utf-8'))
    # Возвращаем хеш в виде шестнадцатеричной строки
    return md5_obj.hexdigest()


engine = create_engine(
    f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4&collation=utf8mb4_general_ci'
)
with open("data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

Base = declarative_base()


class PrsrToilets(Base):
    __tablename__ = 'prsr_toilets'
    id = Column(String(32), primary_key=True)
    address = Column(String(255), nullable=False)
    coordinates = Column(Geometry('POINT'), nullable=False)
    description = Column(Text)


class PrsrImage(Base):
    __tablename__ = 'prsr_toilet_images'
    toilet_id = Column(String(32), primary_key=True)

    image_url = Column(String(1000), primary_key=True)


# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Данные для вставки
new_id = '1234567890abcdef1234567890abcdef'  # пример id (32 символа)
new_address = '123 Main St, City'
new_coordinates_wkt = 'POINT(30.12345 50.54321)'  # WKT формат для POINT
new_description = 'Описание объекта'
try:
    for d in data.values():
        id_ = string_to_md5(d['address'])
        # Создаем объект новой записи
        new_record = PrsrToilets(
            id=id_,
            address=d['address'],
            coordinates=f"POINT({d['coordinates'][0]} {d['coordinates'][1]})" ,
            description=d['titile']
        )

        # Добавляем и коммитим
        session.add(new_record)
        for i in d['images']:
            session.add(PrsrImage(
                toilet_id=id_,
                image_url=i
            ))
    session.commit()
    print("Данные успешно вставлены")
except Exception as e:
    print(f"Ошибка: {e}")
    session.rollback()
finally:
    session.close()
