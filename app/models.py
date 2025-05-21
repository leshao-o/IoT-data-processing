from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# спросить как работает и для чего relationship(back_populates="") 

# 📝 Описание связей (просто словами):
# Один пользователь → много устройств.
# Одно устройство → много сенсоров и много команд.
# Один сенсор → много измерений (sensor_data) и много алертов.
# Все таблицы логически связаны через ключи (FK), чтобы можно было строить иерархию данных по пользователю → устройствам → сенсорам → данным/алертам.

# 📐 Пример сценария использования:
# Пользователь зарегистрировался → создал устройство «Контроллер 1» → добавил 2 сенсора (температура, влажность).
# Сенсоры начали передавать данные → они сохраняются в sensor_data.
# Температура превысила порог → система сгенерировала алерт в alerts.
# Пользователь отправил команду «включить вентилятор» → запись попала в device_commands.


# ✅ Позволяет связать устройства и данные с конкретным пользователем → каждый пользователь видит только свои устройства, сенсоры и данные
class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    devices: Mapped[list["DeviceORM"]] = relationship(back_populates="user")


# Хранит информацию об IoT-устройствах (например, контроллеры, платы, сборочные узлы), зарегистрированных системой
# ✅ Каждое устройство принадлежит пользователю. Через эту таблицу пользователь управляет своими устройствами и их сенсорами
class DeviceORM(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # Название устройства (для отображения, поиска)
    description: Mapped[str] = mapped_column(String(300))  # Описание устройства (тип, местоположение)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # Идентификатор пользователя-владельца устройства
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["UserORM"] = relationship(back_populates="devices")
    sensors: Mapped[list["SensorORM"]] = relationship(back_populates="device")
    commands: Mapped[list["DeviceCommandORM"]] = relationship(back_populates="device")


# Хранит информацию о сенсорах (датчиках), установленных на устройстве
# Например, у одного устройства может быть датчик температуры, влажности, давления
# ✅ Разделяет данные по конкретным сенсорам устройства → в системе можно понимать, какой сенсор передал данные, и обрабатывать их независимо
class SensorORM(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # Название сенсора (например, "Температура 1")
    type: Mapped[str] = mapped_column(String(50))  # Тип сенсора (температура, влажность, свет)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))  # ID устройства, к которому привязан сенсор

    device: Mapped["DeviceORM"] = relationship(back_populates="sensors")
    data: Mapped[list["SensorDataORM"]] = relationship(back_populates="sensor")
    alerts: Mapped[list["AlertORM"]] = relationship(back_populates="sensor")


# Хранит измеренные значения, которые поступают от сенсоров
# Это «сырьевая» таблица данных, на основе которой строятся графики, отчёты, анализ
# ✅ Важна для аналитики, построения трендов, обработки событий
class SensorDataORM(Base):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id"))  # ID сенсора, от которого пришли данные
    value: Mapped[float] = mapped_column()  # Измеренное значение (например, температура)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Время получения данных

    sensor: Mapped["SensorORM"] = relationship(back_populates="data")


# Хранит события/оповещения, которые сгенерированы системой на основе данных сенсоров (например, превышение порога температуры)
# ✅ Сохраняет историю срабатываний → оператор/пользователь может видеть, когда и на каком сенсоре было событие, и как отреагировала система
class AlertORM(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id"))  # ID сенсора, который вызвал алерт
    alert_type: Mapped[str] = mapped_column(String(50))  # Тип алерта (например, "HighTemp")
    description: Mapped[str] = mapped_column(String(300))  # Текстовое описание причины/содержания алерта
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Дата и время создания алерта

    sensor: Mapped["SensorORM"] = relationship(back_populates="alerts")


# Хранит команды, отправленные на устройства (например, включить вентилятор, отключить нагрев)
# ✅ Позволяет отслеживать историю управления устройствами и фиксировать статус исполнения команды
class DeviceCommandORM(Base):
    __tablename__ = "device_commands"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))  # ID устройства, которому отправлена команда
    command: Mapped[str] = mapped_column(String(100))  # Команда (например, "turn_on_fan")
    status: Mapped[str] = mapped_column(String(50), default="pending")  # Статус выполнения (pending, sent, failed)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Дата и время создания команды

    device: Mapped["DeviceORM"] = relationship(back_populates="commands")
