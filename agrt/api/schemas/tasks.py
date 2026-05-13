from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class EnvironmentType(str, Enum):
    PYTHON = "python"
    NODE = "node"
    DOCKER = "docker"
    BARE_METAL = "bare_metal"

class SafetyLevel(str, Enum):
    STRICT = "strict"  # No internet, no file write outside project
    MODERATE = "moderate" # Internet allowed, file write restricted
    OPEN = "open" # Full local access (Admin/Root)

class ExecutionTask(BaseModel):
    id: str = Field(..., description="Unique task identifier")
    objective: str = Field(..., description="The high-level goal of the execution task")
    priority: TaskPriority = TaskPriority.NORMAL
    
    # Context & Requirements
    environment: EnvironmentType = EnvironmentType.PYTHON
    dependencies: List[str] = Field(default_factory=list, description="Required packages or libraries")
    
    # Safety & Boundaries
    safety_level: SafetyLevel = SafetyLevel.STRICT
    max_retries: int = 3
    timeout_seconds: int = 300
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ExecutionReport(BaseModel):
    task_id: str
    success: bool
    execution_time: float
    output: Optional[str] = None
    errors: List[str] = Field(default_factory=list)
    rollback_performed: bool = False
    explainability_token: str = Field(..., description="Token to retrieve detailed execution reasoning")
