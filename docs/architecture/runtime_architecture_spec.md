# Runtime Architecture Specification v5.0 (Autonomous Infrastructure Edition)

## 1. Infrastructure Memory (`/artifacts`)
The platform persists all execution life-cycles as structured "Memory" artifacts. 
- **Telemetry Snapshots**: Low-level event streams for replayability.
- **Benchmark Runs**: Comparative data on model performance and repair success.
- **Repair Logs**: Detailed audit of autonomous self-healing actions.

## 2. Failure Taxonomy & Repair Routing
We use a deterministic **Failure Taxonomy** to map errors to **Repair Capabilities**.
- `DEPENDENCY_FAILURE` -> `DependencyRepair`
- `STYLE_VIOLATION` -> `RuffRepair`
- `STARTUP_FAILURE` -> `LogRepair` (Next)

## 3. Operational Confidence Engine
The system calculates a **Confidence Score** for every execution:
- **Liveness (60%)**: Did the process start and heartbeat?
- **Integrity (20%)**: Did it pass static analysis and ruff?
- **Artifacts (20%)**: Were all expected files created and valid?

## 4. Time-Travel Debugging (UI Engine)
The UI Dashboard supports **Timeline Scrubbing** by replaying the persisted Telemetry Snapshots. This allows developers to "rewind" autonomous orchestration and inspect state-transitions at any micro-step.
