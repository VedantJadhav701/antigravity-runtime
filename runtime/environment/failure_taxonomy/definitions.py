from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class FailureType(str, Enum):
    DEPENDENCY_FAILURE = "dependency_failure"
    SYNTAX_FAILURE = "syntax_failure"
    LINT_FAILURE = "lint_failure"
    IMPORT_FAILURE = "import_failure"
    RUNTIME_FAILURE = "runtime_failure"
    STARTUP_FAILURE = "startup_failure"
    VALIDATION_FAILURE = "validation_failure"
    ORCHESTRATION_FAILURE = "orchestration_failure"
    UNKNOWN_FAILURE = "unknown_failure"

class FailureSignal(BaseModel):
    type: FailureType
    message: str
    context: Dict[str, Any] = {}
    severity: str = "error"
