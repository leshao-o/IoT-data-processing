import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from app.api.auth import router as auth_router
from app.api.device import router as device_router
from app.api.alert import router as alert_router
from app.api.sensor import router as sensor_router
from app.api.sensor_data import router as sensor_data_router
from app.api.device_command import router as device_command_router


app = FastAPI(title="IoT Data Processing API")

app.include_router(auth_router)
app.include_router(device_router)
app.include_router(alert_router)
app.include_router(sensor_router)
app.include_router(sensor_data_router)
app.include_router(device_command_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
