from pathlib import Path
from datetime import datetime
import pickle
from app.logs import logger

folder_path = Path(__file__).resolve().parent
tasks_file_path = folder_path / "tasks.bin"


def load_tasks() -> list:
    tasks_file_path.parent.mkdir(parents=True, exist_ok=True)
    new_tasks_list = []

    if tasks_file_path.exists():
        try:
            with tasks_file_path.open("rb") as file:
                return pickle.load(file)
        except EOFError:
            return new_tasks_list

    else:
        with tasks_file_path.open("wb") as file:
            pickle.dump(new_tasks_list, file)
        return new_tasks_list


def check_match_catalog(user_input: str, prompt: tuple) -> bool:
    if user_input not in prompt:
        print("\nInvalid value. Please enter a valid number.")
        logger.warning(f"User selected an invalid main menu option: {user_input}.")
        print()
        return True
    return False


def create_task(database: list[dict], user_task: str) -> dict:
    id_task = len(database) + 1
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task = {
        "id": str(id_task),
        "title": user_task,
        "time_created": current_datetime,
        "status": "in progress",
    }

    return task


def save_tasks(database: list[dict]) -> None:
    with tasks_file_path.open("wb") as file:
        pickle.dump(database, file)


def add_task(database: list[dict], task: dict) -> None:
    database.append(task)
    save_tasks(database)


def ask_yes_no(prompt: str) -> str:
    while True:
        user_answer = input(prompt).lower().strip()
        if user_answer in ("yes", "no"):
            return user_answer

        print("\nInvalid input! Please select 'yes' or 'no'.")
        logger.warning(f"User entered invalid value - {user_answer}.")
        print()


def view_tasks(database: list[dict]) -> None:
    if len(database) == 0:
        pass
    else:
        print("-" * 40 + "\nList Tasks:\n" + "-" * 40)
        for task in database:
            print(f"Task {task['id']}:")
            print(f"  Title       : {task['title']}")
            print(f"  Created at  : {task['time_created']}")
            print(f"  Status      : {task['status']}")
            print("-" * 40)


def check_empty(database: list[dict]) -> bool:
    if not database:
        print("\nThe task list is empty. Returning to the main menu.")
        logger.warning(
            "The task list is empty. Returning to the main menu."
        )
        print()
        return True
    return False


def find_task(database: list[dict], id_task: str) -> dict | None:
    for task in database:
        if task["id"] == id_task:
            return task
    return None


def check_task_number_input(database: list[dict], id_task: str) -> bool:
    if not find_task(database, id_task):
        print(f"\nTask value '{id_task}' is not found in the database.")
        logger.warning(f"Invalid value entered - {id_task}.")
        print()
        return True
    return False


def get_task_title(database: list[dict], id_task: str) -> str:
    return find_task(database, id_task)["title"]


def editing_task_title(database: list[dict], id_task: str, new_task: str) -> None:
    task = find_task(database, id_task)
    task["title"] = new_task
    save_tasks(database)


def editing_task_status(database: list[dict], id_task: str, new_status: str) -> None:
    task = find_task(database, id_task)
    task["status"] = new_status
    save_tasks(database)


def remove_task(database: list[dict], id_task: str) -> bool | None:
    task = find_task(database, id_task)
    if task:
        database.remove(task)
    else:
        print(f"Task number {id_task} is not found in the database.")
        return False

    for index, task in enumerate(database, start=1):
        task["id"] = str(index)

    save_tasks(database)
    return None
