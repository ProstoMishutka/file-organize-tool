from pathlib import Path
from datetime import datetime
import pickle
from app.logs import logger

# Creating a path to the file for storing user tasks
folder_path = Path(__file__).resolve().parent
tasks_file_path = folder_path / "tasks.bin"


def load_tasks() -> list:
    """
    The function reads the file where the user's task list is stored. If such a file does not exist, the function creates the directory with subdirectories along the file path and returns it empty for writing as a task list.
    :return new_tasks_list(list): User task list
    """
    tasks_file_path.parent.mkdir(parents=True, exist_ok=True)
    new_tasks_list = []

    if tasks_file_path.exists():
        try:
            with tasks_file_path.open("rb") as file:
                return pickle.load(file)
        except EOFError:
            logger.info(
                "An empty list has been created for task storage and management."
            )
            return new_tasks_list

    else:
        with tasks_file_path.open("wb") as file:
            pickle.dump(new_tasks_list, file)
        return new_tasks_list


def check_match_catalog(user_input: str, prompt: tuple) -> bool:
    """
    The function checks the validity of the entered menu task number.
    :param user_input: The value entered by the user (task number).
    :param prompt: Tuple of task items.
    :return: True if the input is invalid, False if it is valid.
    """
    if user_input not in prompt:
        print("\nInvalid value. Please enter a valid number.")
        logger.warning(f"User selected an invalid main menu option: {user_input}.")
        print()
        return True
    return False


def create_task(database: list[dict], user_task: str) -> dict:
    """
    The function takes the user's task text, assigns it a sequential number, creation time, and sets the status to "in progress", then returns all this as a dictionary.
    :param database: User task list as a list of dictionaries.
    :param user_task: Task text.
    :return task(dict): User task dictionary.
    """
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
    """
    The function takes a task list in the form of a list of dictionaries and writes it to a file.
    :param database: User task list as a list of dictionaries.
    :return: None
    """
    with tasks_file_path.open("wb") as file:
        pickle.dump(database, file)


def add_task(database: list[dict], task: dict) -> None:
    """
    The function adds a new task to the task list.
    :param database: User task list as a list of dictionaries.
    :param task: A dictionary where the keys are task ID ("id"), task text ("title"), task creation time ("time_created"), and task status ("status").
    :return: None
    """
    database.append(task)
    save_tasks(database)


def ask_yes_no(prompt: str) -> str:
    """
    The function asks the user to enter yes or no.
    :param prompt: A template text that asks the user whether they want to continue performing the same action.''
    :return user_answer(str): yes or no.
    """
    while True:
        user_answer = input(prompt).lower().strip()
        if user_answer in ("yes", "no"):
            return user_answer

        print("\nInvalid input! Please select 'yes' or 'no'.")
        logger.warning(f"User entered invalid value - {user_answer}.")
        print()


def view_tasks(database: list[dict]) -> None:
    """
    The function displays in the console the list of tasks in the format: task ID ("id"), task text ("title"), task creation time ("time_created"), and task status ("status").
    :param database: User task list as a list of dictionaries.
    :return: None
    """
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
    """
    The function checks the presence of tasks in the list. If the list contains tasks, it returns False; if there are no tasks, it returns True.
    :param database: User task list as a list of dictionaries.
    :return: Returns True if there are no tasks in the list, and False if the list contains tasks.
    """
    if not database:
        print("\nThe task list is empty. Returning to the main menu.")
        logger.warning("The task list is empty. Returning to the main menu.")
        print()
        return True
    return False


def find_task(database: list[dict], id_task: str) -> dict | None:
    """
    The function accepts a task ID, searches the task list for a task with that ID, and returns the corresponding task. If no task with that ID is found, it returns None.
    :param database: User task list as a list of dictionaries.
    :param id_task: Task ID
    :return task(dict) or None: User task dictionary or None.
    """
    for task in database:
        if task["id"] == id_task:
            return task
    logger.warning(f"Task number not found - {id_task}")
    return None


def check_task_number_input(database: list[dict], id_task: str) -> bool:
    """
    The function accepts a task ID, checks its presence in the task list, and returns True if a task with that ID is not found, or False if the task ID exists in the list.
    :param database: User task list as a list of dictionaries.
    :param id_task: Task ID.
    :return: True if a task with that ID is not found, or False if the task ID exists in the list.
    """
    if not find_task(database, id_task):
        print(f"\nTask value '{id_task}' is not found in the database.")
        logger.warning(f"Invalid value entered - {id_task}.")
        print()
        return True
    return False


def get_task_title(database: list[dict], id_task: str) -> str:
    """
    The function takes a task list and a task ID, and returns the text (title) of that task.
    :param database: User task list as a list of dictionaries.
    :param id_task: Task ID.
    :return: Text of the found task.
    """
    return find_task(database, id_task)["title"]


def editing_task_title(database: list[dict], id_task: str, new_task: str) -> None:
    """
    The function takes a task list, a task ID, and new text for editing, and replaces the task's text with the new text.
    :param database: User task list as a list of dictionaries.
    :param id_task: Task ID.
    :param new_task: New task text.
    :return: None
    """
    task = find_task(database, id_task)
    task["title"] = new_task
    save_tasks(database)


def editing_task_status(database: list[dict], id_task: str, new_status: str) -> None:
    """
    The function takes a task list, a task ID, and a new status for editing the task, and replaces the task's status with the new one.
    :param database: User task list as a list of dictionaries.
    :param id_task: Task ID.
    :param new_status: New task status.
    :return: None
    """
    task = find_task(database, id_task)
    task["status"] = new_status
    save_tasks(database)


def remove_task(database: list[dict], id_task: str) -> bool | None:
    """
    The function takes a task list and a task ID, checks if the task exists in the list, and deletes it if present. If a task with that ID is not found, it displays a warning. After deleting the task, the function renumbers the remaining tasks sequentially: 1, 2, 3, 4…
    :param database: User task list as a list of dictionaries.
    :param id_task: Task ID.
    :return: False if task does not exist in the database.
    """
    task = find_task(database, id_task)
    if task:
        database.remove(task)
    else:
        print(f"\nTask number {id_task} is not found in the database.")
        logger.warning(f"Task number {id_task} is not found in the list.")
        print()
        return False

    for index, task in enumerate(database, start=1):
        task["id"] = str(index)

    save_tasks(database)
    return True
