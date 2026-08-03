from pathlib import Path


def find_json_files(root_dir: Path, filename: str):
    """
    Recursively find every JSON file with the given filename.

    Example:
        temperature.json
        frequency.json
    """

    return sorted(root_dir.rglob(filename))