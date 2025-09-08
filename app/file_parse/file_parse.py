from pathlib import Path
import shutil
from datetime import datetime
from app.logs import logger


def to_path(path: str) -> Path:
    """
    The function takes a path as a string and converts it into a Path type.
    :param path: A path of type string.
    :return: A path of type Path.
    """
    return Path(path)


def is_valid_directory(path: Path) -> bool:
    """
    The function checks whether a path exists and is a directory, and returns a boolean value.
    :param path: Path to a directory.
    :return: True if the path exists and is a directory, otherwise False.
    """
    return path.exists() and path.is_dir()


def is_valid_path(path: Path) -> bool:
    """
    Checks whether a path exists and returns the result as a boolean value.
    :param path: Path to a directory or a file.
    :return: True if the path exists, otherwise False.
    """
    return path.exists()


def is_valid_file(path: Path) -> bool:
    """
    The function checks whether the specified path is a file.
    :param path: Path to the file.
    :return: True if the specified path is a file, otherwise False.
    """
    return path.is_file()


def create_folder(path: Path, folder: str) -> Path:
    """
    The function takes a path to a directory and the name of a directory to be created, and creates it if it does not exist.
    :param path: Path to a directory.
    :param folder: The name of the directory to be created.
    :return: Path to the newly created directory of type Path.
    """
    path_for_folder = path / folder
    path_for_folder.mkdir(parents=True, exist_ok=True)
    return path_for_folder


def move_file(item: Path, path_folder: Path) -> None:
    """
    The function takes the path to a file and the destination path, moves the file, and displays a warning if the operation fails.
    :param item: A file in a directory.
    :param path_folder: The directory where the file will be moved.
    :return: None
    """
    try:
        shutil.move(item, path_folder)
    except PermissionError:
        print(f"\nPermission denied: {item} -> {path_folder}")
        logger.warning(f"Permission denied: {item} -> {path_folder}")
        print()
    except FileExistsError:
        print(f"\nFile {item.name} already exists in {path_folder}")
        logger.warning(f"\nFile {item.name} already exists in {path_folder}")
        print()
    except OSError:
        print(f"\nError while moving {item} to {path_folder}")
        logger.warning(f"\nError while moving {item} to {path_folder}")
        print()


def sort_by_file_type(path: Path) -> None:
    """
    The function sorts files by their type, creating a corresponding folder for each file type. If a file has no extension, it is placed in a folder named NO_EXTENSION.
    :param path: Path to the directory whose files will be sorted.
    :return: None
    """
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
    """
    The function sorts files by their last modification date, organizing them into folders by month in the YYYY-MM format.
    :param path: Path to the directory whose files will be sorted.
    :return: None
    """
    for item in path.iterdir():
        if item.is_dir():
            continue

        seconds = item.stat().st_mtime
        to_datetime = datetime.fromtimestamp(seconds)
        new_name_folder = datetime.strftime(to_datetime, "%Y-%m")

        path_folder = create_folder(path, new_name_folder)
        move_file(item, path_folder)

    print("Sorting completed")


def read_file(path: Path) -> str | None:
    try:
        if path.suffix == ".txt" or path.suffix == ".log":
            with open(path, "r", encoding="utf-8") as file:
                text = file.read()
        elif path.suffix == ".bin":
            with open(path, "rb") as file:
                text = file.read()
        else:

            try:
                with open(path, "r", encoding="utf-8") as file:
                    unknown_text = file.read()
                print(unknown_text)
            except Exception as e:
                print(f"\nFile open error – {e}.")
                logger.error(f"File open error – {e}.")
                print()

        print()
        return "File content:\n" + text

    except FileNotFoundError:
        print(f"\nFile {path.name} not found")
        logger.warning(f"File {path.name} not found")
        print()
        return None


def remove_file(path: Path, recursive: bool) -> None:
    """
    The function deletes a directory or file. If the directory contains any content, it asks for permission to delete it along with its contents.
    :param path: Path to the directory or file to be deleted.
    :param recursive: A flag that allows deleting a directory with its contents: if the flag is True, deletion of the directory and its contents is permitted; if False, deletion is prohibited.
    :return: None
    """
    if path.is_dir():
        if recursive:
            shutil.rmtree(path)
        else:
            path.rmdir()

    if path.is_file():
        path.unlink(missing_ok=True)
