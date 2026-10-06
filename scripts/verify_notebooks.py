"""Execute the teaching notebooks and save outputs only in the solution copy."""

from __future__ import annotations

import asyncio
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@contextmanager
def working_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def execute(path: Path, save_outputs: bool) -> None:
    notebook = nbformat.read(path, as_version=4)
    with working_directory(NOTEBOOK_DIR):
        NotebookClient(
            notebook,
            timeout=300,
            kernel_name="python3",
            allow_errors=False,
            record_timing=False,
        ).execute()

    if save_outputs:
        nbformat.write(notebook, path)
    print(f"PASS: {path.name}")


def main() -> None:
    execute(NOTEBOOK_DIR / "field_to_evidence_student.ipynb", save_outputs=False)
    execute(NOTEBOOK_DIR / "field_to_evidence_solutions.ipynb", save_outputs=True)
    execute(NOTEBOOK_DIR / "evaluate_any_classifier_template.ipynb", save_outputs=False)


if __name__ == "__main__":
    main()
