# custom_tool.py
from crewai.tools import BaseTool
from pydantic import Field
import os
import re
from typing import Optional

class SaveFileTool(BaseTool):
    """
    Saves provided content to a file under a configured base directory.

    You can call with either:
      - path="<relative/path/with/filename.ext>"
      OR
      - directory="<relative/dir>" and filename="<file.ext>"

    Safety:
      - Ensures writes remain within 'base_dir'
      - Creates parent directories if needed
      - Overwrite policy: 'fail' | 'overwrite' | 'dedupe'
    """
    name: str = "save_file"
    description: str = (
        "Saves provided content to a local file path. Use with either "
        "`path` OR `directory` + `filename`. Returns the absolute saved path."
    )

    # Tool configuration (validated once when tool is instantiated)
    base_dir: str = Field(default="outputs", description="Base directory for saves")
    default_filename: str = Field(default="index.md", description="Default filename used when only a directory is provided")

    def _run(
        self,
        content: str,
        path: Optional[str] = None,
        directory: Optional[str] = None,
        filename: Optional[str] = None,
        mode: str = "overwrite",
    ) -> str:
        """
        Args:
            content: File contents to write.
            path: Relative file path (e.g., 'articles/foo.md' or 'articles/').
            directory: Relative directory under base_dir (e.g., 'articles/2026-01-27').
            filename: File name (e.g., 'why-small-teams-ship-faster.md'). If missing extension, '.md' is added.
            mode: 'fail' | 'overwrite' | 'dedupe'

        Returns:
            Confirmation message with the absolute saved path.
        """
        # Resolve final relative path (under base_dir)
        rel = self._resolve_relative_path(path=path, directory=directory, filename=filename)
        final_abs = self._join_and_secure(rel)

        # Ensure directory exists
        parent = os.path.dirname(final_abs)
        if parent:
            os.makedirs(parent, exist_ok=True)

        # Resolve overwrite policy
        final_abs = self._apply_overwrite_policy(final_abs, mode)

        # Write content
        with open(final_abs, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Saved file to: {final_abs}"

    # -------------------------
    # Internal helpers
    # -------------------------
    def _resolve_relative_path(
        self,
        path: Optional[str],
        directory: Optional[str],
        filename: Optional[str],
    ) -> str:
        # 1) If 'path' is provided, normalize and decide if it’s a dir or file
        if path:
            norm = self._normalize_rel(path)
            # If 'path' points to an existing dir or looks like a dir (no dot in the last segment),
            # append default filename.
            if os.path.isdir(norm) or "." not in os.path.basename(norm):
                # Treat as a directory
                norm_dir = norm
                safe_name = self._ensure_filename(self.default_filename)
                return os.path.join(norm_dir, safe_name).replace("\\", "/")
            # Otherwise, it's a file path
            return norm

        # 2) Else, require directory + filename
        if not directory and not filename:
            raise ValueError(
                "Provide either `path` or both `directory` and `filename`."
            )

        dir_norm = self._normalize_rel(directory or ".")
        file_norm = self._ensure_filename(filename or self.default_filename)
        return os.path.join(dir_norm, file_norm).replace("\\", "/")

    def _ensure_filename(self, name: str) -> str:
        # Slugify + ensure extension (.md default if none)
        name = self._slugify_filename(name)
        if "." not in os.path.basename(name):
            name = f"{name}.md"
        return name

    def _slugify_filename(self, name: str) -> str:
        """
        Keep only lowercase letters, numbers, dots, underscores, and hyphens.
        Convert spaces to hyphens, collapse repeats, strip edges.
        """
        base = os.path.basename(name)
        base = base.strip().lower()
        base = re.sub(r"[ \t\n\r]+", "-", base)
        base = re.sub(r"[^a-z0-9._-]", "-", base)
        base = re.sub(r"-{2,}", "-", base).strip("-")
        return base or "untitled.md"

    def _normalize_rel(self, rel_path: str) -> str:
        """Normalize a relative path (no traversal/absolute). Returns a POSIX-like relative path."""
        if rel_path is None:
            return "."
        norm = os.path.normpath(rel_path).replace("\\", "/")
        # Disallow absolute paths or traversal outside base_dir
        if norm.startswith("../") or norm.startswith("/") or ":" in norm:
            raise ValueError("Refused: path must be a safe relative path.")
        return norm

    def _join_and_secure(self, rel: str) -> str:
        """Join base_dir + rel and ensure final path is inside base_dir."""
        base_abs = os.path.abspath(self.base_dir)
        final_abs = os.path.abspath(os.path.join(base_abs, rel))
        # Ensure the final path stays within base_abs
        if not final_abs.startswith(base_abs + os.sep) and final_abs != base_abs:
            raise ValueError("Refused: final path escapes the base directory.")
        return final_abs

    def _apply_overwrite_policy(self, final_abs: str, mode: str) -> str:
        mode = (mode or "overwrite").lower()
        if os.path.exists(final_abs):
            if mode == "fail":
                raise FileExistsError(f"Refused: file already exists at {final_abs}")
            elif mode == "dedupe":
                base, ext = os.path.splitext(final_abs)
                i = 1
                candidate = f"{base}-{i}{ext}"
                while os.path.exists(candidate):
                    i += 1
                    candidate = f"{base}-{i}{ext}"
                return candidate
            # overwrite (default) continues
        return final_abs