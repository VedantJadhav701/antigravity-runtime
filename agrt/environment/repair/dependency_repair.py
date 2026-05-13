import re
import logging
from typing import Optional
from agrt.shared.interfaces.base import SandboxInterface, RepairInterface

logger = logging.getLogger("agrt.repair.dependency")

class DependencyRepair(RepairInterface):
    """
    Workflow: Dependency Resolution
    1. Detect: ModuleNotFoundError: No module named 'X'
    2. Action: Extract X.
    3. Execute: pip install X within the Sandbox.
    4. Retry: Re-run the original command (handled by orchestrator).
    """
    
    # Pattern to match ModuleNotFoundError and extract the module name
    # Example: ModuleNotFoundError: No module named 'requests'
    # Example: ImportError: No module named 'requests'
    DEP_PATTERN = re.compile(r"(?:ModuleNotFoundError|ImportError): No module named '([^']+)'")

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.repair_counts = {} # track retries per module/session

    async def repair(self, failure_context: dict, sandbox: SandboxInterface) -> bool:
        """
        Attempts to repair a dependency-related failure.
        failure_context should contain 'stderr' and potentially 'session_id'.
        """
        stderr = failure_context.get("stderr", "")
        session_id = failure_context.get("session_id", "default")
        
        match = self.DEP_PATTERN.search(stderr)
        if not match:
            logger.debug("No dependency error detected in stderr")
            return False
            
        module_name = match.group(1)
        logger.info(f"Detected missing dependency: {module_name}")
        
        # Escalation Policy check
        retry_key = f"{session_id}:{module_name}"
        current_retries = self.repair_counts.get(retry_key, 0)
        
        if current_retries >= self.max_retries:
            logger.error(f"Max retries reached for dependency: {module_name}")
            return False
            
        # Action: pip install X
        # Note: We use the sandbox's execute_command which should use the venv's pip
        # if the sandbox is a VenvProvider.
        # We'll assume the command 'pip install' is enough if the environment is set up.
        # However, to be safe, VenvProvider should handle the context.
        
        logger.info(f"Attempting to install missing module: {module_name}")
        # Use python -m pip for reliability
        install_result = await sandbox.execute_command(f"python -m pip install {module_name}")
        
        if install_result["exit_code"] == 0:
            self.repair_counts[retry_key] = current_retries + 1
            logger.info(f"Successfully installed {module_name}")
            return True
        else:
            logger.error(f"Failed to install {module_name}: {install_result['stderr']}")
            return False
