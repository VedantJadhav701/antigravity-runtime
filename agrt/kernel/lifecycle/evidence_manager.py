import json
import os
import logging
from datetime import datetime
from agrt.kernel.lifecycle.evidence import ExecutionEvidence

logger = logging.getLogger("agrt.kernel.evidence")

class EvidenceManager:
    """
    Handles the persistence and retrieval of 'Flight Logs'.
    """
    def __init__(self, storage_dir: str = ".agrt/history"):
        self.storage_dir = os.path.abspath(storage_dir)
        os.makedirs(self.storage_dir, exist_ok=True)

    def persist(self, evidence: ExecutionEvidence) -> str:
        """
        Saves the evidence to a JSON file.
        Returns the path to the saved file.
        """
        task_dir = os.path.join(self.storage_dir, evidence.task_id)
        os.makedirs(task_dir, exist_ok=True)
        
        file_path = os.path.join(task_dir, "report.json")
        
        try:
            with open(file_path, "w") as f:
                f.write(evidence.model_dump_json(indent=2))
            logger.info(f"Execution Evidence persisted: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to persist evidence: {e}")
            return ""

    def load(self, task_id: str) -> Optional[ExecutionEvidence]:
        """
        Loads evidence from disk.
        """
        file_path = os.path.join(self.storage_dir, task_id, "report.json")
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return ExecutionEvidence(**data)
        except Exception as e:
            logger.error(f"Failed to load evidence: {e}")
            return None
