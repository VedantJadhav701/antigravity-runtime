from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from runtime.api.websocket.handler import TelemetryManager
from runtime.kernel.lifecycle.engine import LifecycleEngine
from runtime.kernel.execution_graph.schemas import TaskSpec
from runtime.api.schemas.tasks import ExecutionReport
import logging

# Initialize Infrastructure
app = FastAPI(title="Runtime Platform Core")
telemetry = TelemetryManager()
kernel = LifecycleEngine(telemetry)

@app.post("/tasks")
async def create_task(task: TaskSpec):
    """
    Entry point for the Runtime Kernel.
    Dispatches task specifications to the Lifecycle Engine.
    """
    return await kernel.run_task(task)

@app.websocket("/ws/telemetry")
async def telemetry_endpoint(websocket: WebSocket):
    await telemetry.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        telemetry.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
