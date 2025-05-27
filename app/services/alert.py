from app.schemas.alert import AlertAdd
from app.services.base import BaseService


class AlertService(BaseService):
    async def get_alerts(self, sensor_id: int):
        return await self.db.alert.get_filtered(sensor_id=sensor_id)
    
    async def add_alert(self, alert_data: AlertAdd):
        new_alert = await self.db.alert.add(data=alert_data)
        await self.db.commit()
        return new_alert
    