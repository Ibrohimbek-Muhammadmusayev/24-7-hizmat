import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LiveMapConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "live_map_group"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Broadcast message to live map group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'location_update',
                'data': data
            }
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'LOCATION_UPDATE',
            'data': event['data']
        }))

    async def order_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ORDER_STATUS_UPDATE',
            'order': event['order']
        }))

class WorkerAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.worker_id = self.scope['url_route']['kwargs']['worker_id']
        self.group_name = f"worker_alerts_{self.worker_id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def new_job_alert(self, event):
        await self.send(text_data=json.dumps({
            'type': 'NEW_JOB_ALERT',
            'order': event['order']
        }))
