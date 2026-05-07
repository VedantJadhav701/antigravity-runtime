from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FailureType(str, Enum):
    DEPENDENCY_FAILURE = "dependency_failure"
    SYNTAX_FAILURE = "syntax_failure"
    LINT_FAILURE = "lint_failure"
    IMPORT_FAILURE = "import_failure"
    STARTUP_FAILURE = "startup_failure"
    VALIDATION_FAILURE = "validation_failure"
    ORCHESTRATION_FAILURE = "orchestration_failure"

class FailureClassification(BaseModel):
    type: FailureType
    severity: str # LOW, MEDIUM, CRITICAL
    source_node: str
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ConfidenceReport(BaseModel):
    score: int # 0-100
    reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=lambda: 0.0)
