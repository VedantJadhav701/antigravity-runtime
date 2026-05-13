import os
import json
import logging
from typing import Dict, Optional

logger = logging.getLogger("agrt.generation.templates")

class TemplateSelector:
    """
    Maps high-level categories to specific scaffold templates.
    """
    MAPPING = {
        "api": "fastapi-basic",
        "web": "react-tailwind-basic",
        "cli": "python-cli-basic"
    }

    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir

    def get_template_path(self, category: str) -> Optional[str]:
        template_name = self.MAPPING.get(category.lower())
        if not template_name:
            logger.error(f"No template found for category: {category}")
            return None
        
        template_path = os.path.join(self.templates_dir, template_name)
        if not os.path.exists(template_path):
            logger.error(f"Template directory does not exist: {template_path}")
            return None
            
        return template_path

    def get_metadata(self, category: str) -> Optional[Dict]:
        path = self.get_template_path(category)
        if not path:
            return None
            
        metadata_path = os.path.join(path, "metadata.json")
        if not os.path.exists(metadata_path):
            return {}
            
        try:
            with open(metadata_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load metadata for {category}: {e}")
            return {}
