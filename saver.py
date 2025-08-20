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

local_port = 3307  # замените на ваш локальный порт

engine = create_engine(
    f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4&collation=utf8mb4_general_ci'
)

Base = declarative_base()


class PrsrToilets(Base):
    __tablename__ = 'prsr_toilets'
    id = Column(String(32), primary_key=True)
    address = Column(String(255), nullable=False)
    coordinates = Column(Geometry('POINT'), nullable=False)
    description = Column(Text)


# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Данные для вставки
new_id = '1234567890abcdef1234567890abcdef'  # пример id (32 символа)
new_address = '123 Main St, City'
new_coordinates_wkt = 'POINT(30.12345 50.54321)'  # WKT формат для POINT
new_description = 'Описание объекта'

try:
    # Создаем объект новой записи
    new_record = PrsrToilets(
        id=new_id,
        address=new_address,
        coordinates=new_coordinates_wkt,
        description=new_description
    )

    # Добавляем и коммитим
    session.add(new_record)
    session.commit()
    print("Данные успешно вставлены")
except Exception as e:
    print(f"Ошибка: {e}")
    session.rollback()
finally:
    session.close()