import json
import os
from pathlib import Path
from typing import Iterable


def save_raw_matches(
    matches: Iterable[dict], batch_index: int, output_dir: str = "data/raw_matches"
):
    """
    Save a batch of raw match JSONs to a .jsonl file.

    Args:
        matches (Iterable[dict]): List or generator of match dicts.
        batch_index (int): Index for file naming (e.g. 0 → matches_000.jsonl).
        output_dir (str): Folder to save batches in.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = Path(output_dir) / f"matches_{batch_index:03}.jsonl"

    with open(file_path, "w", encoding="utf-8") as f:
        for match in matches:
            json.dump(match, f)
            f.write("\n")
