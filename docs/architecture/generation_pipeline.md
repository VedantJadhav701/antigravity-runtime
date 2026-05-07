# Generation Engine: Execution Pipeline

## 1. Step 1: Task Classification (The Filter)
- **Input**: User prompt (e.g., "Build a todo app").
- **LLM Prompt**: "Classify this request into one of: [PYTHON_CLI, FASTAPI_API, REACT_UI, FULLSTACK_SAAS]."
- **Output**: `ProjectCategory`.

## 2. Step 2: Template Selection (The Anchor)
- Mapping `ProjectCategory` to `TemplateID`.
- If `FULLSTACK_SAAS` -> Use `saas-starter`.

## 3. Step 3: Feature Extraction (The Composition)
- Identify keywords in the prompt to trigger **Injectors**.
- Keywords: "Login", "User", "Account" -> Trigger `auth` injector.
- Keywords: "Payment", "Price", "Buy" -> Trigger `stripe` injector.

## 4. Step 4: Plan Synthesis (The Blueprint)
- Generate the `ExecutionPlan` JSON.
- This plan is passed to the **Orchestrator**.

## 5. Step 5: Execution Grounding (The Grounding)
- **Scaffold**: Copy template files to the Sandbox.
- **Inject**: Apply patches to files (e.g., adding `auth_middleware` to `main.py`).
- **Validate**: Sandbox runs `python -m server` to check if the injected code actually executes.
- **Repair**: If `ImportError` occurs (e.g., missing `PyJWT`), trigger the **Repair Loop**.
