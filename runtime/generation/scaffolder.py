import os
import shutil
import logging
from typing import Optional

logger = logging.getLogger("runtime.generation.scaffolding")

class ProjectScaffolder:
    """
    Handles the physical creation of project structures based on templates.
    """
    def __init__(self, templates_dir: Optional[str] = None):
        if not templates_dir:
            # Default to the templates directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.join(current_dir, "templates")
            
        self.templates_dir = templates_dir

    def scaffold(self, template_id: str, destination: str) -> bool:
        """
        Copies all files from the specified template to the destination directory.
        Includes path safety checks to prevent traversal.
        """
        if not self._is_safe_path(destination):
            logger.error(f"Security Violation: Destination path {destination} is outside allowed boundaries.")
            return False

        template_path = os.path.join(self.templates_dir, template_id)
        # ... rest of the method
        if not os.path.exists(template_path):
            logger.error(f"Template not found: {template_path}")
            return False
            
        try:
            logger.info(f"Scaffolding project from {template_id} to {destination}")
            os.makedirs(destination, exist_ok=True)
            
            for item in os.listdir(template_path):
                s = os.path.join(template_path, item)
                d = os.path.join(destination, item)
                
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            
            return True
        except Exception as e:
            logger.error(f"Failed to scaffold project: {e}")
            return False

    def _is_safe_path(self, path: str) -> bool:
        """
        Ensures the path is within the project workspace or a temporary directory.
        Prevents traversal to sensitive system directories.
        """
        # For simplicity in this skeleton, we verify it doesn't contain traversal patterns
        # In production, this would check against a WHITELIST_ROOT.
        return ".." not in path and not path.startswith("/") and not path.startswith("\\")
