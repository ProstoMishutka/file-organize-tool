from app.logs import logger
from app.organize import *


def check_match_catalog(user_input: str, prompt: tuple) -> bool:
    """
    The function checks the validity of the entered menu task number.
    :param user_input: The value entered by the user (task number).
    :param prompt: Tuple of task items.
    :return: True if the input is invalid, False if it is valid.
    """
    if user_input not in prompt:
        print("\nInvalid value. Please enter a valid number.")
        logger.warning(f"The user entered an invalid value: {user_input}.")
        print()
        return True
    return False


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


def select_option(database: list[dict], prompt: str) -> str:
    """
    The function displays the list of tasks on the screen, asks the user which task they choose, and returns its index in the list.
    :param database: User task list as a list of dictionaries.
    :param prompt: Prompt to the user to select the task's sequential number.
    :return id_task: The task's sequential number from the list.
    """
    while True:
        view_tasks(database)
        logger.debug(f"Task List: {database}")

        id_task = input(prompt)
        logger.info(f"The user selected task number {id_task}.")
        if not check_task_number_input(database, id_task):
            return id_task


def ask_continue(prompt: str) -> bool:
    """
    The function asks the user whether they want to continue working on tasks with the same action (e.g., editing).
    :param prompt: A template text that asks the user whether they want to continue performing the same action.
    :return: True if the user wants to continue the task action, otherwise False.
    """
    user_answer = ask_yes_no(prompt).lower().strip()

    if user_answer == "no":
        logger.info("User returned to the main menu.")
        print()
        return False

    logger.info(f"User selected: {prompt}")
    return True
