import logging
from typing import List, Set

logger = logging.getLogger("runtime.generation.merger")

class RequirementsMerger:
    """
    Consolidates multiple dependency specifications into a single unique list.
    """
    
    def merge_files(self, file_paths: List[str]) -> List[str]:
        """
        Reads multiple requirements.txt files and returns a deduplicated list of dependencies.
        Warns if multiple versions of the same package are detected.
        """
        merged_deps: Set[str] = set()
        seen_packages = {}
        
        for path in file_paths:
            try:
                with open(path, "r") as f:
                    for line in f:
                        dep = line.strip()
                        if dep and not dep.startswith("#"):
                            # Simple conflict detection: check package name before '==' or '>='
                            name = dep.split("=")[0].split(">")[0].strip().lower()
                            if name in seen_packages and seen_packages[name] != dep:
                                logger.warning(f"Dependency Conflict: Multiple versions for '{name}': {seen_packages[name]} vs {dep}")
                            
                            seen_packages[name] = dep
                            merged_deps.add(dep)
            except Exception as e:
                logger.error(f"Failed to read requirements file {path}: {e}")
                
        return sorted(list(merged_deps))

    def merge_lists(self, dep_lists: List[List[str]]) -> List[str]:
        """
        Consolidates multiple lists of dependencies into a single deduplicated list.
        """
        merged_deps: Set[str] = set()
        
        for dep_list in dep_lists:
            for dep in dep_list:
                clean_dep = dep.strip()
                if clean_dep and not clean_dep.startswith("#"):
                    merged_deps.add(clean_dep)
                    
        return sorted(list(merged_deps))

    def write_merged(self, dependencies: List[str], output_path: str) -> bool:
        """
        Writes a list of dependencies to a requirements.txt file.
        """
        try:
            with open(output_path, "w") as f:
                for dep in dependencies:
                    f.write(f"{dep}\n")
            return True
        except Exception as e:
            logger.error(f"Failed to write merged requirements: {e}")
            return False
