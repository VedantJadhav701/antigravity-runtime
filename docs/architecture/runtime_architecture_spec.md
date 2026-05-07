# Runtime Architecture Specification v5.2 (Runtime Hygiene Edition)

## 1. The Quarantine Lifecycle (`.runtime/quarantine/`)
To preserve operational trust, the kernel never performs `rm -rf` on an active or recently failed session. Instead, it "Quarantines" the session.

### Quarantine Process:
1. **Identify**: Mark session as `STALE` or `FAILED`.
2. **Move**: Relocate the session directory to `.runtime/quarantine/{session_id}/`.
3. **Annotate**: Create a `quarantine_metadata.json` including:
   - `reason`: (e.g., Timeout, Rollback, Manual Purge)
   - `timestamp`: Time of quarantine.
   - `final_state`: The last known state of the execution graph.
4. **Audit Window**: Keep the session in quarantine for a configurable period (default: 7 days).

## 2. Orphan Cleanup (GC)
The **CleanupManager** runs as a background task to identify and resolve:
- **Orphan Processes**: Processes whose parent graph is no longer active.
- **Dead Venvs**: Virtual environments that haven't been touched in > 24h.
- **Abandoned Sessions**: Sessions that reached a final state but weren't finalized.

## 3. Permanent Disposal
After the audit window expires, the system performs a **Deterministic Purge** of the quarantine zone to reclaim disk space.
