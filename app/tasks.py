# from celery import Celery
# from sqlalchemy.orm import sessionmaker
# from .database import engine
# from . import crud, schemas

# celery = Celery('tasks', broker='redis://localhost:6379/0')

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @celery.task
# def process_sensor_data(sensor_data: dict):
#     db = SessionLocal()
#     try:
#         data_in = schemas.SensorDataIn(**sensor_data)
#         db_data = crud.create_sensor_data(db, data_in)
        
#         # Пример бизнес-логики (алерт при высокой температуре)
#         if data_in.type == 'temperature' and data_in.value > 40:
#             crud.create_alert(db, sensor_id=data_in.sensor_id, alert_type='HighTemp', description=f"Температура {data_in.value}")
        
#         db.close()
#     except Exception as e:
#         db.close()
#         raise e
