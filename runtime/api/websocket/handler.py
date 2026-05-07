import json
import logging
from typing import List
from fastapi import WebSocket

logger = logging.getLogger("runtime.telemetry")

class TelemetryManager:
    """
    Manages active WebSocket connections and broadcasts execution events.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected to Telemetry. Active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected from Telemetry. Active: {len(self.active_connections)}")

    async def broadcast_event(self, source: str, phase: str, event_type: str, message: str, data: dict = None):
        """
        Broadcasting structured telemetry to all connected UIs.
        """
        payload = {
            "source": source,
            "phase": phase,
            "event_type": event_type,
            "message": message,
            "data": data or {}
        }
        
        # Cleanup closed connections while broadcasting
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(payload))
            except Exception:
                disconnected.append(connection)
                
        for conn in disconnected:
            self.disconnect(conn)
