import asyncio
import logging
import psutil
import os
import signal

logger = logging.getLogger("agrt.kernel.watchdog.termination")

async def terminate_process_tree(pid: int, timeout_sec: float = 5.0) -> bool:
    """
    v5.1 Utility: Handles graceful and forced termination of orphaned or timed-out processes.
    Attempt graceful termination (SIGTERM), then escalate to SIGKILL.
    """
    try:
        parent = psutil.Process(pid)
        # Terminate children first
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        
        try:
            parent.terminate()
        except psutil.NoSuchProcess:
            return True # Parent already gone

        # Wait for graceful exit
        all_procs = children + [parent]
        _, alive = psutil.wait_procs(all_procs, timeout=timeout_sec)
        
        if alive:
            logger.warning(f"Process tree for {pid} still alive after {timeout_sec}s, escalating to SIGKILL")
            for p in alive:
                try:
                    p.kill()
                except psutil.NoSuchProcess:
                    pass
        
        return True
    except psutil.NoSuchProcess:
        return True # Already gone
    except Exception as e:
        logger.error(f"Failed to terminate process tree {pid}: {e}")
        return False

class ProcessTerminator:
    """Legacy wrapper for terminate_process_tree"""
    @staticmethod
    async def terminate(pid: int, timeout_sec: float = 5.0) -> bool:
        return await terminate_process_tree(pid, timeout_sec)
