import json
import os
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class QuarantineMetadata(BaseModel):
    """
    Metadata for an environment moved to the quarantine zone.
    """
    session_id: str
    reason: str
    timestamp: datetime = Field(default_factory=datetime.now)
    final_graph_state: Optional[str] = None
    exit_code: Optional[int] = None
    last_node_action: Optional[str] = None

def save_quarantine_metadata(target_dir: str, metadata: QuarantineMetadata):
    """
    Persists metadata into the quarantined session directory.
    """
    meta_path = os.path.join(target_dir, "quarantine_metadata.json")
    with open(meta_path, "w") as f:
        f.write(metadata.model_dump_json(indent=2))
