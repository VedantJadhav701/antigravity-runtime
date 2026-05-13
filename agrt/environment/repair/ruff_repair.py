import logging
import subprocess
import re
from agrt.shared.interfaces.base import SandboxInterface, RepairInterface

logger = logging.getLogger("agrt.repair.ruff")

class RuffRepair(RepairInterface):
    """
    Workflow: Static Analysis Repair
    1. Detect: Ruff violation in stderr or failure context.
    2. Action: Run ruff check --fix on the affected file.
    """
    async def repair(self, failure_context: dict, sandbox: SandboxInterface) -> bool:
        stderr = failure_context.get("stderr", "")
        # Check if ruff violation is mentioned (as added by ValidationEngine)
        if "Ruff violation" not in stderr:
            return False
            
        # Try to extract file path
        # Example: Ruff violation in C:\...\server.py: ...
        match = re.search(r"Ruff violation in (.*?\.py):", stderr)
        if not match:
            return False
            
        file_path = match.group(1).strip()
        logger.info(f"Detected Ruff violation in {file_path}. Attempting autonomous fix...")
        
        try:
            # Run ruff check --fix
            result = subprocess.run(
                ["ruff", "check", "--fix", file_path, "--no-cache"],
                capture_output=True,
                text=True
            )
            # Ruff exits with 0 if it fixed everything or if there's nothing left
            # We'll check if the file is fixed by running validation again (handled by loop)
            if result.returncode == 0:
                logger.info(f"Ruff repair cycle completed for {file_path}")
                return True
            else:
                # Even if returncode is not 0, some fixes might have been applied.
                # But we'll report failure if it couldn't fix the issues.
                logger.warning(f"Ruff could not fix all issues in {file_path}: {result.stdout or result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error running ruff fix: {e}")
            return False
