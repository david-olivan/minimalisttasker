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

    tasks = load_tasks(db_name)

    new_screen(tasks)

    while True:
        accept_command(input("Introduce a command: "), tasks, db_name)


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
        case "remove":
            tasks = remove_task(tasks)
            new_screen(tasks, "The task has been removed.")
        case _:
            new_screen(tasks, "That is not a valid command.")


def get_commands():
    """
    Displays all available commands that can be given to the program

    :return: The list of commands appropriately formatted
    :rtype: str
    """
    return "\nCommands:\t new\t save\t remove\t exit\n"


def new_task(tasks: list) -> Task:
    """
    Creates a new task, checks that the name is not longer than 100 char
    and priority is an int 1-5 and returns it

    :param tasks: The list of tasks currently available
    :type tasks: list
    :return: A newly created task using the Task object
    :rtype: Task
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

    :param tasks: The current list of tasks
    :type tasks: list
    :return: The updated list of tasks sans the given task
    :rtype: list
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


def display_tasks(tasks: list):
    """
    Uses the list of Task objects to display available tasks for the user
    in order of priority with an index number

    :param tasks: The list of Task objects with the tasks
    :type tasks: list
    """
    desglosada = []
    for task in sort_by_priority(tasks):
        desglosada.append([task.the_id, task.priority, task.name])

    print(tabulate(desglosada, headers=["Id", "Priority", "Name"]))


def sort_by_priority(lista):
    """
    Uses the sorted function to sort tasks by priority as a key

    :param lista: The list to be sorted
    :type lista: list
    :return: The sorted list
    :rtype: list
    """
    return sorted(lista, key=lambda task: task.priority)


def save_tasks(tasks: list, database: str):
    """
    Saves the files being worked on on the .csv database

    :param tasks: The current list of tasks
    :type tasks: list
    :param database: The name of the database where the tasks ought to be saved
    :type database: str
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


def load_tasks(database: str) -> list:
    """
    Opens the csv file, loads the tasks and return them as a list of Task objects

    :param database: The name of the csv file that has been selected
    :type database: str
    :return: The list of tasks extracted from the database
    :rtype: list
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

    :param text: The text to be formatted as a heading
    :type text: str
    :return: The three line string with the text as a heading
    :rtype: str
    """
    line1 = "\t\t***" + ("*" * len(text)) + "***\n"
    line2 = "\t\t*  " + text.upper() + "  *\n"
    line3 = "\t\t***" + ("*" * len(text)) + "***"

    return line1 + line2 + line3


def clear_screen():
    """
    Clears the screen based on os without showing the os.system eeeevery time
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_name() -> str:
    """
    Gets an input from the user and verifies it as a valid name

    :return: A string with the valid, verified name of the database
    :rtype: str
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

    :param name: The name of the database
    :type name: str
    :return: Whether there is a database with that name or not
    :rtype: bool
    """
    if os.path.isfile(f"users/{name}.csv"):
        return True
    else:
        return False


def is_name_valid(name: str) -> bool:
    """
    Checks if a given name is valid
    (i.e. only letters and numbers,underscores and hyphens permitted)

    :param name: The name to be examined
    :type name: str
    :return: Whether the name is valid or not
    :rtype: bool
    """
    if re.match(r"^[A-Za-z0-9_-]*$", name):
        return True
    else:
        return False


def create_database(name: str):
    """
    Creates a database with headers in users/ folder

    :param name: The name of the new database
    :type name: str
    """
    with open("users/" + name + ".csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "priority", "id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def parse_arguments() -> str:
    """
    Parse arguments and return database name or lack thereof

    :return: A string representing the database name or the fact that there isn't one.
    :rtype: str
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
