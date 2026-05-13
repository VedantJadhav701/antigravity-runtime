import logging
import json
import os
from typing import List, Dict, Any, Optional
from agrt.kernel.execution_graph.schemas import TaskSpec

logger = logging.getLogger("agrt.planner.compiler")

class TaskSpecCompiler:
    """
    Validates and compiles intent data into an infrastructure-grade TaskSpec.
    Orchestration truth is derived from the Planner Registry.
    """
    def __init__(self, registry_path: Optional[str] = None):
        if not registry_path:
            # Default to the system registry
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            registry_path = os.path.join(base_dir, "registry", "definitions.json")
            
        with open(registry_path, "r") as f:
            self.registry = json.load(f)

    def compile(self, 
                project_type: str, 
                template_id: str, 
                features: List[str] = None,
                environment: Dict[str, Any] = None,
                constraints: List[str] = None) -> TaskSpec:
        """
        Validates inputs against the registry and produces a TaskSpec.
        Raises ValueError if validation fails.
        """
        logger.info(f"Compiling TaskSpec for template: {template_id}")

        # Validate Template exists in registry
        if template_id not in self.registry["templates"]:
            raise ValueError(f"Orchestration Violation: Unsupported template '{template_id}'")

        template_def = self.registry["templates"][template_id]

        # Validate Features (Injectors)
        validated_features = []
        for feature_id in (features or []):
            if feature_id not in self.registry["injectors"]:
                logger.warning(f"Feature '{feature_id}' not found in registry. Skipping.")
                continue
            
            # Check compatibility with template
            if feature_id not in template_def.get("allowed_injectors", []):
                raise ValueError(f"Orchestration Violation: Feature '{feature_id}' is incompatible with template '{template_id}'")
            
            validated_features.append(feature_id)

        spec = TaskSpec(
            project_type=project_type,
            template_id=template_id,
            features=validated_features,
            environment=environment or {},
            constraints=constraints or [],
            metadata={
                "compiler_version": "2.0",
                "registry_id": self.registry.get("metadata", {}).get("id", "default"),
                "validation_status": "passed"
            }
        )

        return spec
