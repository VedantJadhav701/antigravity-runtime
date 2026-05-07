# Failure-to-Action Mapping (The Repair Matrix)

This table defines how the `RepairEngine` classifies and reacts to Static Analysis (Ruff) violations.

| Error Code (Ruff) | Classification | Autonomous Action |
|-------------------|----------------|-------------------|
| `F401` (Unused Import) | Optimization | Remove unused import line |
| `E999` (Syntax Error) | Critical | Trigger AI "Heal" or Rollback |
| `F821` (Undefined Name) | Missing Dep | Infer package from name -> `pip install` |
| `I001` (Import Sort) | Linting | Run `ruff --fix` |
| `D100` (Missing Doc) | Warning | Ignore (Standard) / Inject Template Doc |

## The Proactive Repair Loop Logic:
1. **Analyze**: Run Ruff check on the scaffolded project.
2. **Classify**: Map the first error code to an Autonomous Action.
3. **Execute**: Perform the `pip install` or `ast` modification.
4. **Verify**: Re-run Ruff. If clean, proceed to `EXECUTING` phase.
