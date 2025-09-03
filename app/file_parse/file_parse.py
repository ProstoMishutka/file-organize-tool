from pathlib import Path
import shutil
from datetime import datetime


def to_path(path: str) -> Path:
    return Path(path)


def is_valid_directory(path: Path) -> bool:
    return path.exists() and path.is_dir()


def is_valid_path(path: Path) -> bool:
    return path.exists()


def create_folder(path: Path, folder: str) -> Path:
    path_for_folder = path / folder
    path_for_folder.mkdir(parents=True, exist_ok=True)
    return path_for_folder


def move_file(item: Path, path_folder: Path) -> None:
    try:
        shutil.move(item, path_folder)
    except PermissionError:
        print(f"Permission denied: {item} -> {path_folder}")
    except FileExistsError:
        print(f"File {item.name} already exists in {path_folder}")
    except OSError:
        print(f"Error while moving {item} to {path_folder}")


def sort_by_file_type(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            continue

        suffix_file = item.suffix
        new_suffix = suffix_file.replace(".", "").upper() or "NO_EXTENSION"
        new_name_folder = f"folder {new_suffix}"

        path_folder = create_folder(path, new_name_folder)
        move_file(item, path_folder)

    print("Sorting completed")


def sort_by_file_date(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            continue

        seconds = item.stat().st_mtime
        to_datetime = datetime.fromtimestamp(seconds)
        new_name_folder = datetime.strftime(to_datetime, "%Y-%m")

        path_folder = create_folder(path, new_name_folder)
        move_file(item, path_folder)

    print("Sorting completed")


def remove_file(path: Path, recursive: bool) -> None:
    if path.is_dir():
        if recursive:
            shutil.rmtree(path)
        else:
            path.rmdir()

    if path.is_file():
        path.unlink(missing_ok=True)
