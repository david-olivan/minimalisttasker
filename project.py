"""
An app that will help you keep track of those tasks that are importante to you
without encouraging an endless list of tasks that never ned. Priorities included!
"""
import re
import sys
import csv
import os
import argparse
from time import sleep
from tabulate import tabulate
from lib.helpers import Task

APP_NAME: str = "The Minimalist Tasker"


def main():
    """
    The main function of the app
    """
    db_name = parse_arguments()
    db_name = check_database(db_name)

    tasks = load_tasks(db_name)

    new_screen(tasks)

    while True:
        accept_command(input("Introduce a command: "), tasks, db_name)


def check_database(db_name) -> str:
    """
    This function gets a database name and finds if there exists one or not and if so selects it.
    If there isn't a database it creates a new one.

    Parameters
    ----------
    db_name : str
        The name to be verified

    Returns
    ----------
    db_name : str
        A verified name or a new name if no-database was the original string
    """
    if db_name == "no-database":
        print("No path selected. Select a database.")

        db_name = get_name()

        if database_exists(db_name):
            print("Database found. Loading the program.")
            sleep(2)
        else:
            print("Creating new database")
            create_database(db_name)
    else:
        print("Path included. Checking for existing databases.")

        if is_name_valid(db_name) and database_exists(db_name):
            print("Database found. Loading the program.")
            sleep(2)
        elif is_name_valid(db_name):
            print("Creating new database")
            create_database(db_name)
        else:
            sys.exit("Database name incorrect.")
    return db_name


def accept_command(cmd: str, tasks: list, database: str) -> None:
    """
    Get a command from the user and process it based on options

    Parameters
    ----------
    cmd : str
        The command that the user typed.
    tasks : list[Task]
        The list of tasks being worked on.
    database : str
        The name of the currently open database.
    """
    match cmd.strip().lower():
        case "exit":
            if input(
                "Do you want to save the current tasks before exiting? (yes/no) "
            ).strip().lower() in ["yes", "y"]:
                save_tasks(tasks, database)
            clear_screen()
            sys.exit(f"Thank you for using {APP_NAME}.")
        case "new":
            tasks.append(new_task(tasks))
            new_screen(tasks)
        case "save":
            if input(
                "Saving will overwrite the file. Are you sure you want to save? (yes/no) "
            ).strip().lower() in ["yes", "y"]:
                save_tasks(tasks, database)
                new_screen(tasks, "The current tasks have been saved.")
            else:
                new_screen(tasks, "Tasks have not been saved.")
        case "modify":
            tasks = modify_task(tasks)
            new_screen(tasks, "The task priority has been modified.")
        case "remove":
            tasks = remove_task(tasks)
            new_screen(tasks, "The task has been removed.")
        case _:
            new_screen(tasks, "That is not a valid command.")


def modify_task(tasks) -> list[Task]:
    """
    Allows the user to modify the priority of a task

    Parameters
    ----------
    tasks : list[Task]
        The current list of tasks.

    Returns
    ----------
    tasks : list[Task]
        The new list of tasks.
    """
    clear_screen()
    print(get_title("Modify Task"))
    display_tasks(tasks)

    while True:
        the_id = input(
            "\nIntroduce the id of the task whose priority you want to modify: "
        ).strip()
        try:
            the_id = int(the_id)
        except ValueError:
            print("The id is not a number.")
        else:
            for task in tasks:
                if task.the_id == the_id:
                    index = tasks.index(task)
                    while True:
                        try:
                            new_priority = int(
                                input("Introduce the new priority for the task: ")
                            )
                        except ValueError:
                            print("The new priority is not a number.")
                        else:
                            if 0 < new_priority < 6:
                                modified_task = Task(
                                    task.name, new_priority, task.the_id
                                )
                                tasks.remove(tasks[index])
                                tasks.append(modified_task)
                                return tasks
                            else:
                                print("Priority is not between 1 and 5.")
            print("No id was found.")


def get_commands() -> str:
    """
    Displays all available commands that can be given to the program

    Returns
    ----------
    str
        The list of commands with tab spaces between keywords.
    """
    return "\nCommands:\t new\t save\t modify remove\t exit\n"


def new_task(tasks: list) -> Task:
    """
    Creates a new task, checks that the name is not longer than 100 char
    and priority is an int 1-5 and returns it

    Parameters
    ----------
    tasks : list[Task]
        The list of tasks currently available.

    Returns
    ----------
    Task
        A newly created task using the Task object.
    """
    clear_screen()
    print(get_title("New Task"))

    while True:
        name = input("Task name (100 characters): ")
        # When creating a new task, cap it to 100 characters (provisional length)
        if len(name) < 101:
            while True:
                # If it's not too long, ask for priority
                try:
                    priority = int(input("Task priority (1-5): "))
                    if 0 < priority < 6:
                        current_ids = []
                        for task in tasks:
                            current_ids.append(task.the_id)

                        the_id = 0
                        while the_id in current_ids:
                            the_id += 1

                        return Task(name, priority, the_id)
                    else:
                        print("Priority is not 1 to 5.")
                except ValueError:
                    print("The priority is not a number.")
        else:
            print("Name is longer than 100 characters.")


def remove_task(tasks: list) -> list[Task]:
    """
    Removes a given task from the list then returns the updated list

    Parameters
    ----------
    tasks : list[Task]
        The current list of tasks.

    Returns
    ----------
    tasks : list[Task]
        The updated list of tasks sans the removed task.
    """
    clear_screen()
    print(get_title("Remove Task"))
    display_tasks(tasks)

    while True:
        the_id = input("\nIntroduce the id of the task you want to remove: ").strip()
        try:
            the_id = int(the_id)
        except ValueError:
            print("The id is not a number.")
        else:
            for task in tasks:
                if task.the_id == the_id:
                    index = tasks.index(task)
                    tasks.remove(tasks[index])
                    return tasks
            print("No id was found.")


def display_tasks(tasks: list) -> None:
    """
    Uses the list of Task objects to display available tasks for the user
    in order of priority with an index number

    Parameters
    ----------
    tasks : list[Task]
        The list of Task objects with the current tasks.
    """
    desglosada = []
    for task in sort_by_priority(tasks):
        desglosada.append([task.the_id, task.priority, task.name])

    print(tabulate(desglosada, headers=["Id", "Priority", "Name"]))


def sort_by_priority(lista) -> None:
    """
    Uses the sorted function to sort tasks by priority as a key

    Parameters
    ----------
    list : list[Task]
        The list to be sorted.

    Returns
    ----------
    list[Task]
        The list, sorted by priority.
    """
    return sorted(lista, key=lambda task: task.priority)


def save_tasks(tasks: list, database: str):
    """
    Saves the files being worked on on the .csv database

    Parameters
    ----------
    tasks : list[Task]
        The current list of tasks.
    database : str
        The name of the database where the tasks ought to be saved
    """
    with open(f"users/{database}.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "priority", "id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(
                {"name": task.name, "priority": task.priority, "id": task.the_id}
            )

    print("List of tasks saved.")
    sleep(1)


def load_tasks(database: str) -> list[Task]:
    """
    Opens the csv file, loads the tasks and return them as a list of Task objects

    Parameters
    ----------
    database : str
        The name of the csv file that has been selected.

    Returns
    ----------
    tasks : list[Task]
        The list of tasks extracted from the database.
    """
    tasks = []
    with open(f"users/{database}.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tasks.append(Task(row["name"], int(row["priority"]), int(row["id"])))
    return tasks


def new_screen(tasks: list, message: str = None) -> None:
    """
    Clears the screen, displays the tasks and the commands as well as an optional message.
    It serves as a way of reducing three lines to one for a lot of commands and options

    Parameters
    ----------
    tasks : list[Task]
        The list of Task objects that is the available tasks.
    message : str, default None
        An optional message for the user.
    """
    clear_screen()
    print(get_title(APP_NAME))
    display_tasks(tasks)
    print(get_commands())
    if message is not None:
        print(message)


def get_title(text: str) -> str:
    """
    Gets a text and formats it as a heading

    Parameters:
    text : str
        The text to be formatted as an app heading

    Returns
    ----------
    line1 + line2 + line3 : str
        The three line string with the text as a heading.
    """
    line1 = "\t\t***" + ("*" * len(text)) + "***\n"
    line2 = "\t\t*  " + text.upper() + "  *\n"
    line3 = "\t\t***" + ("*" * len(text)) + "***"

    return line1 + line2 + line3


def clear_screen() -> None:
    """
    Clears the screen based on os without showing the os.system eeeevery time
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_name() -> str:
    """
    Gets an input from the user and verifies it as a valid name following the conventions.
    Rules are only letters, numbers, hyphens and underscores. No spaces.

    Returns
    ----------
    name : str
        A string with a valid, verified name according to conventions,
    """
    while True:
        # Ask user for a database name
        name = input("Introduce a name (no spaces): ")

        # Verify that it doesn't have spaces or other unwanted symbols
        if is_name_valid(name):
            return name
        else:
            print(
                "That name is incorrect. Only letters, numbers, hyphens and underscores allowed."
            )


def database_exists(name: str) -> bool:
    """
    Checks if a database exists in users/ folder

    Parameters
    ----------
    name : str
        The name of the database to be checked.

    Returns
    ----------
    True/False : bool
        Whether there is a database with that name or not.
    """
    if os.path.isfile(f"users/{name}.csv"):
        return True
    else:
        return False


def is_name_valid(name: str) -> bool:
    """
    Checks if a given name is valid
    (i.e. only letters and numbers,underscores and hyphens permitted)

    Parameters
    ----------
    name : str
        The name to be examined to see if it is valid.

    Returns
    ----------
    True/False : bool
        Whether the name is valid or not
    """
    if re.match(r"^[A-Za-z0-9_-]*$", name):
        return True
    else:
        return False


def create_database(name: str) -> None:
    """
    Creates a database with headers in users/ folder

    Parameters
    ----------
    name : str
        The name of the new database to be created.
    """
    with open("users/" + name + ".csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "priority", "id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def parse_arguments() -> str:
    """
    Parse arguments and return database name or lack thereof

    Returns
    ----------
    args.filename : str
        A string representing the database name or the fact that there isn't one.
    """
    parser = argparse.ArgumentParser(
        prog="project.py", description="Manage all your projects and tasks."
    )
    parser.add_argument(
        "filename",
        nargs="?",
        default="no-database",
        help="Your projects and tasks .csv database",
        type=str,
    )
    args = parser.parse_args()

    return args.filename


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(f"Application closed. Thank you for using {APP_NAME}.")
