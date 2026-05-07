import os
import logging
from typing import Optional, Dict
from runtime.generation.templates.selector import TemplateSelector

logger = logging.getLogger("runtime.generation.planners")

class BasePlanner:
    """
    Base class for generation planning.
    Responsible for selecting templates and defining the scaffolding strategy.
    """
    def __init__(self, templates_dir: Optional[str] = None):
        if not templates_dir:
            # Default to the templates directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.join(os.path.dirname(current_dir), "templates")
            
        self.selector = TemplateSelector(templates_dir)

    def select_template(self, category: str) -> Optional[str]:
        """
        Selects a template name based on the requested category.
        """
        logger.info(f"Selecting template for category: {category}")
        template_path = self.selector.get_template_path(category)
        
        if template_path:
            return os.path.basename(template_path)
        return None

    def get_plan_metadata(self, category: str) -> Dict:
        """
        Retrieves metadata for the selected template category.
        """
        return self.selector.get_metadata(category) or {}
