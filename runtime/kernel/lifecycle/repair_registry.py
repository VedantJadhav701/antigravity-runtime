from typing import Dict, List, Type
from runtime.shared.interfaces.base import RepairInterface
from runtime.environment.repair.dependency_repair import DependencyRepair
from runtime.environment.repair.ruff_repair import RuffRepair
from runtime.environment.failure_taxonomy.definitions import FailureType

class RepairRegistry:
    """
    Capability-based repair selection.
    Maps FailureTypes to prioritized lists of repair strategies.
    """
    def __init__(self):
        self.registry: Dict[FailureType, List[RepairInterface]] = {
            FailureType.DEPENDENCY_FAILURE: [DependencyRepair(max_retries=3)],
            FailureType.IMPORT_FAILURE: [DependencyRepair(max_retries=3)],
            FailureType.LINT_FAILURE: [RuffRepair()],
            FailureType.SYNTAX_FAILURE: [RuffRepair()], # Ruff can fix some syntax-related style
            FailureType.VALIDATION_FAILURE: [RuffRepair()] # Generic validation might trigger ruff fix
        }

    def get_repairers(self, failure_type: FailureType) -> List[RepairInterface]:
        return self.registry.get(failure_type, [])
