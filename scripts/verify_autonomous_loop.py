import asyncio
import logging
import os
import shutil
from runtime.kernel.lifecycle.engine import LifecycleEngine
from runtime.kernel.execution_graph.schemas import TaskSpec
from runtime.api.websocket.handler import TelemetryManager

# Configure logging
logging.basicConfig(level=logging.INFO)

async def verify_autonomous_loop():
    # 1. Setup
    telemetry = TelemetryManager()
    engine = LifecycleEngine(telemetry)
    
    # 2. Define Task Spec (Deliberately NOT including 'fastapi' to trigger repair)
    spec = TaskSpec(
        project_type="api",
        template_id="fastapi_basic",
        features=[] # 'fastapi' is missing!
    )
    
    print("\n--- Starting Autonomous Loop Verification ---")
    report = await engine.run_task(spec)
    
    print(f"\nExecution Report: {report.model_dump()}")
    
    if report.success:
        print("\n✅ SUCCESS: The autonomous loop completed, likely after self-healing.")
    else:
        print("\n❌ FAILURE: The autonomous loop failed.")

    # 3. Cleanup
    # Optional: shutil.rmtree(".runtime/sessions")

if __name__ == "__main__":
    asyncio.run(verify_autonomous_loop())
