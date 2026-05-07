"""WebSocket connection manager for broadcasting list mutations."""

import json
from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    """Track active WebSocket connections grouped by list_id."""

    def __init__(self) -> None:
        self._connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, list_id: str, websocket: WebSocket) -> None:
        """Accept and register a WebSocket connection for a list."""
        await websocket.accept()
        self._connections[list_id].append(websocket)

    def disconnect(self, list_id: str, websocket: WebSocket) -> None:
        """Remove a WebSocket connection from the registry."""
        self._connections[list_id].remove(websocket)
        if not self._connections[list_id]:
            del self._connections[list_id]

    async def broadcast(self, list_id: str, message: dict) -> None:
        """Send a JSON message to all connections on a given list."""
        payload = json.dumps(message)
        for websocket in list(self._connections.get(list_id, [])):
            await websocket.send_text(payload)


manager = ConnectionManager()
