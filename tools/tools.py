# tools.py
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any
from crewai.tools import tool


# from config import Config


# -------------------------------------------------------------------
# Configuration: restrict file operations to a workspace root
# Set CREW_WORKSPACE to sandbox I/O (recommended in prod/servers).
# If not set, defaults to current working directory.
# -------------------------------------------------------------------
WORKSPACE_ROOT = "/workspaces/acn-dmgumagay-project-agentic-asset/"


def _resolve_safe(path_like: str) -> Path:
    """
    Resolve a path against WORKSPACE_ROOT and ensure it doesn't escape it.
    """
    p = (WORKSPACE_ROOT / path_like).resolve()
    try:
        p.relative_to(WORKSPACE_ROOT)
    except ValueError:
        # Path traversal attempt outside sandbox
        raise ValueError(
            f"Path '{p}' escapes workspace '{WORKSPACE_ROOT}'. "
            "Refuse to operate outside the configured workspace."
        )
    return p

@tool("create_directory_tool")
def create_directory_tool(path: str) -> Dict[str, Any]:
    """
    Create a directory if it does not exist.

    Args:
        path: Directory path relative to the workspace root, for example:
              "artifacts/reports/2026-01" or "./out".

    Behavior:
        - If the directory already exists, it won't be recreated.
        - If it does not exist, it is created with parents=True.

    Returns (dict):
        {
          "path": "<absolute_path>",
          "existed": <bool>,
          "created": <bool>,
          "message": "<status message>"
        }

    Usage guidance for the LLM:
        - Provide a clean, relative path (no .. segments).
        - Example call arguments:
            {"path": "outputs/run_001"}
    """
    d = _resolve_safe(path)
    existed = d.exists()
    if not existed:
        d.mkdir(parents=True, exist_ok=True)
        created = True
        msg = f"Directory created: {d}"
    else:
        created = False
        msg = f"Directory already exists: {d}"

    return {
        "path": str(d),
        "existed": existed,
        "created": created,
        "message": msg,
    }

@tool("write_file_tool")
def write_file_tool(file_path: str, content: str, ensure_parent: bool = True) -> Dict[str, Any]:
    """
    Write text content to a file (always overwrite).

    Args:
        file_path: File path relative to the workspace root, e.g., "outputs/report.txt".
        content:   The full text to write into the file.
        ensure_parent: If True, create the parent directory if missing (default: True).

    Behavior:
        - Opens the file in text mode with UTF-8 encoding and 'w' (overwrite).
        - Optionally creates the parent directory.
        - Returns byte count written.

    Returns (dict):
        {
          "path": "<absolute_path>",
          "bytes_written": <int>,
          "message": "File written (overwritten) successfully."
        }

    Usage guidance for the LLM:
        - Always pass the full desired text for the file.
        - Example call arguments:
            {"file_path": "outputs/summary.txt", "content": "<your text>"}
    """
    fpath = _resolve_safe(file_path)
    parent = fpath.parent
    if ensure_parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)

    # Always overwrite
    # Note: Use newline normalization as needed (here we write as-is).
    encoded = content.encode("utf-8")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "path": str(fpath),
        "bytes_written": len(encoded),
        "message": "File written (overwritten) successfully."
    }
