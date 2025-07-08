from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str, user_id: str):
        await websocket.accept()
        
        # Add to tenant connections
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = []
        self.active_connections[tenant_id].append(websocket)
        
        # Track user connection
        self.user_connections[user_id] = websocket
        
        logger.info(f"WebSocket connected: user {user_id} in tenant {tenant_id}")

    def disconnect(self, websocket: WebSocket, tenant_id: str, user_id: str):
        # Remove from tenant connections
        if tenant_id in self.active_connections:
            if websocket in self.active_connections[tenant_id]:
                self.active_connections[tenant_id].remove(websocket)
            
            # Clean up empty tenant lists
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]
        
        # Remove user connection
        if user_id in self.user_connections:
            del self.user_connections[user_id]
        
        logger.info(f"WebSocket disconnected: user {user_id} in tenant {tenant_id}")

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.user_connections:
            try:
                await self.user_connections[user_id].send_text(message)
            except Exception as e:
                logger.error(f"Error sending personal message to {user_id}: {e}")

    async def broadcast_to_tenant(self, message: str, tenant_id: str):
        if tenant_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[tenant_id]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to tenant {tenant_id}: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected connections
            for connection in disconnected:
                self.active_connections[tenant_id].remove(connection)

    async def broadcast_event(self, event_data: dict, tenant_id: str):
        message = json.dumps({
            "type": "event",
            "data": event_data
        })
        await self.broadcast_to_tenant(message, tenant_id)

    async def broadcast_alert(self, alert_data: dict, tenant_id: str):
        message = json.dumps({
            "type": "alert",
            "data": alert_data
        })
        await self.broadcast_to_tenant(message, tenant_id)

    async def broadcast_camera_status(self, camera_data: dict, tenant_id: str):
        message = json.dumps({
            "type": "camera_status",
            "data": camera_data
        })
        await self.broadcast_to_tenant(message, tenant_id)

    def get_connection_count(self, tenant_id: str) -> int:
        return len(self.active_connections.get(tenant_id, []))

# Global connection manager instance
manager = ConnectionManager()