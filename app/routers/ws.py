"""WebSocket handler for real-time list updates."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.broadcast import manager

router = APIRouter()


@router.websocket("/ws/{list_id}")
async def websocket_endpoint(list_id: str, websocket: WebSocket):
    """Accept a WebSocket connection and keep it open until the client disconnects."""
    await manager.connect(list_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(list_id, websocket)
