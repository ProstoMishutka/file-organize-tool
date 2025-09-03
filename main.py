from app.organize import *
from app.file_parse import *
from app.logs import logger


def main():
    base_menu = (
        "--- File Organize Tool ---\n"
        "1. Add task\n"
        "2. View tasks\n"
        "3. Edit task\n"
        "4. Delete task\n"
        "5. File operations\n"
        "6. Exit"
    )

    database_tasks = load_tasks()

    while True:
        print(base_menu)
        logger.info(f"Main menu displayed: {[item for item in base_menu.split("\n")]}")
        user_input = input("Select an action and enter its number: ").strip()
        print()

        catalog = ("1", "2", "3", "4", "5", "6")
        if check_match_catalog(user_input, catalog):
            continue

        if user_input == "1":
            logger.info("User selected action: Add Task.")

            while True:
                user_task = (
                    input("Enter the description of your task: ").capitalize().strip()
                )
                if not user_task:
                    logger.warning("User entered an empty string.")
                    print("Task cannot be empty!\n")
                elif len(user_task) > 200:
                    logger.warning("User input too long (over 200 characters).")
                    print("Task cannot be longer than 200 characters!\n")
                elif any(
                    user_task.capitalize() == task["title"] for task in database_tasks
                ):
                    logger.warning(
                        f"User tried to add a task that already exists - {user_task}."
                    )
                    print("T2ask already exists!\n")
                else:
                    add_task(database_tasks, create_task(database_tasks, user_task))
                    logger.info(f"Task added successfully: {user_task}.")
                    print(f"Task added successfully: {user_task}.\n")

                    user_answer = (
                        ask_yes_no("Add another task? yes/no: ").lower().strip()
                    )

                    if user_answer == "no":
                        logger.info("User returned to the main menu.")
                        print()
                        break

                    logger.info("User selected: Add another task.")

        elif user_input == "2":
            logger.info("User selected action: View Tasks.")
            if check_empty(database_tasks):
                continue

            view_tasks(database_tasks)
            logger.info(f"The user successfully viewed the task list")
            print()

        elif user_input == "3":
            logger.info("User selected action: Edit Task.")
            if check_empty(database_tasks):
                continue

            edit_menu = "--- Edit menu ---\n" \
                        "1. Edit task\n" \
                        "2. Edit task status\n" \
                        "3. Back"

            while True:
                print(edit_menu)
                logger.debug(f"The menu has opened: {[item for item in edit_menu.split("\n")]}")

                user_selection = input("Choose an edit option and enter the number: ").strip()
                logger.info(f"The user entered - {user_selection}")
                print()

                catalog = ("1", "2", "3")
                if check_match_catalog(user_selection, catalog):
                    continue

                if user_selection == "1":
                    logger.info("The user selected option 1 - 'Task Editing'.")
                    while True:
                        view_tasks(database_tasks)
                        logger.debug(f"Task List: {database_tasks}")

                        id_task = input("Enter the number of the task you want to edit: ")
                        logger.info(f"The user selected task number {id_task}.")
                        if check_task_number_input(database_tasks, id_task):
                            continue

                        old_title = find_task(database_tasks, id_task)["title"]
                        replace_task = (
                            input("Enter the new title of the task: ").capitalize().strip()
                        )
                        editing_task_title(database_tasks, id_task, replace_task)
                        logger.info(f"Task edited successfully: {old_title} -> {replace_task}.")
                        print("Task successfully updated.\n")

                        user_answer = ask_yes_no("Edit another task? yes/no: ")

                        if user_answer == "no":
                            logger.info("User returned to the main menu.")
                            print()
                            break

                        logger.info("User selected: Edit another task.")

                elif user_selection == "2":
                    logger.info("User selected action: Edit task status.")

                    while True:
                        view_tasks(database_tasks)
                        logger.debug(f"Task List: {database_tasks}")

                        id_task = input("Enter the number of the task you want to edit: ")
                        logger.info(f"The user selected task number {id_task}.")
                        if check_task_number_input(database_tasks, id_task):
                            continue

                        old_status = find_task(database_tasks, id_task)["status"]
                        while True:
                            new_status = (
                                input("Enter the new status (in progress/done/paused) of the task: ").lower().strip()
                            )
                            if new_status not in ("in progress", "done", "paused"):
                                print()
                                print(f"Invalid value entered - {new_status}.")
                                logger.warning(f"Invalid value entered - {new_status}.")
                                print()
                                continue

                            break

                        editing_task_status(database_tasks, id_task, new_status)
                        logger.info(f"Task status changed successfully {old_status} -> {new_status}.")
                        print("Task successfully updated.\n")

                        user_answer = ask_yes_no("Edit another task? yes/no: ")

                        if user_answer == "no":
                            logger.info("User returned to the main menu.")
                            print()
                            break

                        logger.info("User selected: Edit another task.")

                elif user_selection == "3":
                    logger.info("User returned to the main menu.")
                    break

        elif user_input == "4":
            logger.info("User selected action: Delete Task.")
            if check_empty(database_tasks):
                continue

            while True:
                view_tasks(database_tasks)
                id_task = input("Enter the number of your task: ").strip()
                if check_task_number_input(database_tasks, id_task):
                    continue

                task_title = find_task(database_tasks, id_task)["title"]
                logger.info(
                    f"User selected to delete task number {id_task} - '{task_title}'."
                )
                remove_task(database_tasks, id_task)
                logger.info(f"Task '{task_title}' deleted successfully.")
                print(f"Deleted task '{task_title}' successfully.\n")

                user_answer = ask_yes_no("Delete another task? yes/no: ")

                if user_answer == "no":
                    logger.info("User returned to the main menu.")
                    print()
                    break

                logger.info("User selected: Add another task.")

                if check_empty(database_tasks):
                    break

        elif user_input == "5":
            menu_work_with_files = (
                "\n--- File Menu Manager ---\n"
                "1. Sort files\n"
                "2. Read files\n"
                "3. Delete files\n"
                "4. Back"
            )

            menu_sort_files = (
                "\n--- Sort File Menu ---\n"
                "1.Sort by file type\n"
                "2.Sort by date\n"
                "3.Back"
            )

            while True:
                print(menu_work_with_files)
                user_input = input(
                    "Select an action to work with files and enter its number: "
                ).strip()

                if user_input == "1":
                    while True:
                        print(menu_sort_files)
                        sorting_option = input(
                            "Choose a sorting option and enter its number: "
                        ).strip()

                        if not sorting_option.isdigit() or sorting_option not in (
                            "1",
                            "2",
                            "3",
                        ):
                            print("Invalid input!")
                            continue

                        if sorting_option == "3":
                            break

                        else:
                            while True:
                                path_for_sort = input(
                                    r"Enter the absolute path of the directory to sort files: "
                                )
                                if not is_valid_directory(to_path(path_for_sort)):
                                    print("Invalid input path!")
                                    continue
                                break

                            path_directory = to_path(path_for_sort)
                            if sorting_option == "1":
                                sort_by_file_type(path_directory)
                                break

                            if sorting_option == "2":
                                sort_by_file_date(path_directory)
                                break

                elif user_input == "3":
                    while True:
                        path_to_remove = input("Enter the absolute path to remove: ")
                        str_to_path = to_path(path_to_remove)
                        if not is_valid_path(str_to_path):
                            print("Invalid input path!")
                            continue

                        if str_to_path.is_dir() and any(str_to_path.iterdir()):
                            answer = (
                                input(
                                    "Warning: the directory has data inside. Proceed with deletion? (yes/no): "
                                )
                                .lower()
                                .strip()
                            )

                            if answer != "no":
                                remove_file(str_to_path, recursive=True)
                                break

                            else:
                                print("Operation cancelled.")
                                break

                        else:
                            remove_file(str_to_path, recursive=False)
                            break

                elif user_input == "4":
                    break

        elif user_input == "6":
            break


if __name__ == "__main__":
    logger.info("Program started")
    main()
