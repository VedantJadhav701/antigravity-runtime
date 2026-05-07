from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ExecutionEvidence(BaseModel):
    """
    The 'Flight Log' of an autonomous task.
    Stored in .runtime/history/{task_id}/report.json
    """
    task_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    task_spec: Dict[str, Any]
    
    # The Full Graph History
    graph_snapshot: Dict[str, Any]
    telemetry_stream: List[Dict[str, Any]]
    
    # Environment Metadata
    environment: Dict[str, Any] = {
        "provider": "VenvProvider",
        "python_version": "3.10+",
        "dependencies": []
    }
    
    # The Judge's Verdict
    validation_summary: Dict[str, Any] = {
        "static_analysis": "PENDING",
        "runtime_validation": "PENDING",
        "repair_count": 0
    }
    
    final_status: str # COMPLETED, FAILED, ROLLBACK
