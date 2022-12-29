# THE MINIMALIST TASKER
#### Video Demo:  <URL https://youtu.be/7DqoUWQLA6U>
#### **Description**: The purpose of this project is to create a simple terminal application that allows the user to create a **database** for their **tasks**, either an individual one or one for each project. The app will use the database to **load**, **save** and **store** the tasks which will be added to it, each with a **priority** level, an automatically generated **id** and a task **description**. The app will present these *tasks* in a table, **ordered** by priority and allow the user to add **new tasks**, **remove** the completed ones and **modify** either the priority of the tasks once created.
---
---
# WELCOME TO **THE MINIMALIST TASKER**
This section will discuss the different [features](#features) of this project, the [packages](#some-packages-it-uses) that have been used, some of the struggles and difficulties, the reasoning behind certain decisions as well as [further development](#further-development) ideas, and how the [documentation](#creating-the-documentation) was carried out, in as much detail as is deemed appropriate for a project of this size and scope. Thank you for reading them!

## FEATURES
There are a few features that have been implemented, but not too many, it's still a minimalist app, after all. ;) Said features allows The Minimalist Tasker to handle projects and tasks in a very simple way. First of all, it lets us either launch the application from the command line using just "python" and the name of the .py file. Then, it asks us for the name of the database we want to use. Alternatively, we can write that name as an argument right after the .py filename when launching the application. Any other combination of arguments or lack thereof will be met with reproach by the handy argparse, both when giving a database name directly or after launching. This is so because the app will check arguments first and then if such a name follows the naming rules established in the app using the re module. If it doesn't, it'll let the user know and prompt them for a new name. If the name is valid, however, the app will next check if a database with that name exists, in which case it will load it, or if it doesn't, it'll create it in the appropriate folder and set it with an example task and the appropriate headings.

### A word on the databases used
As part of the planning process for this project, a decision on which file system for the database to store the tasks had to be made. After some considerations .csv files were chosen due to the easiness in which they may be used for information that does not have a lot of volume. SQL-like databases were discarded since they did not seem to add a lot to a project with few tasks and each task with very few bits of information. Thus, the time invested in taming a more complex file system was deemed more appropriately allocated to the myriad other things that had to be learnt and applied.

### What happens after loading the database
If the database has any tasks stored inside, they will be loaded onto a list made up of [Task objects (a class created for this project)](#a-class-just-for-this-app) and said list will be ordered and presented to the user by passing it to a dedicated function. Most of the functionally was slowly refactored out of main() and into their own independent functions and the display_tasks() was one such change.

Another dedicated function is called accept_command() and its function is to call the display tasks and present the user with a prompt in which certain commands may be passed. Using a switch it will test those inputs against the cases and allow the user to select different operations such as [creating a new task](#creating-a-new-task), [removing a task](#removing-a-task), [modifying a task](#modifying-a-task), [saving](#saving) the current list of tasks or exiting the application.

### Creating a new task
Even though the example.csv file contains a number of tasks as examples of what the app can do, when a user creates a new database it will only be populated by the example task. That is not a problem, because one of the features is the creation of new tasks. When using this option the title at the top of the text within the terminal will change (using a function to maintain the asterisk box around it) and the app will prompt the user for the name of the task and the priority the user wants to assign to it, checking that the name is not longer than a 100 characters and the priority is a number between 1 and 5, both included, and letting the user know when these conditions have not been met.

Then, it will create a Task object with the information, assign it an id number that is not present in the current list of tasks, and add this Task object to said list, returning it to main so that it can be used to display the updated list to the user.

### Removing a task
The option is given to remove a task when it has been completed or it is no longer relevant. Selecting this command will load a new screen where the unique id of the task to be removed will be asked. Checks have been made to make sure it is a valid id. After a valid id is selected, the task will be removed from the current list of tasks, and when saving, those changes will take effect on the .csv database.

### Modifying a task
If the priority of a task changes, the app allows the user to change it. Selecting the modify command will load another screen where the user will be asked to provide the unique id of the task to be modified. After a validity check, a new priority will be introduced and, given that it's a valid number, the current list of tasks will be updated.

## Saving
In order to save the current list of tasks to the .csv, the user has to select the save options from the main screen of the app. This will start a function that, after a prompt so that the user confirms if they want to save the current tasks, will loop through the Task objects and rewrite the .csv database with the current tasks, after transforming each Task object to a dict that will be written as a row to the .csv.

When choosing to exit the app, the user will also be prompted to choose whether to save or not the tasks, just in case they have forgotten to do so.

## SOME PACKAGES IT USES
As with most app, this one was built on work done by other people by way of the modules and packages (both installed through pip and already present in a basic python installation), which makes work so much easier because there is not need to devise a way of validating user input against a pattern if there is a module that already handles that functionality for you, which frees your time, focus and effort towards developing those things that are the core of the app and makes it distinctive.

### Packages that need no installation
Some of the packages that were employed in the developing of this app are the **_sys_** and **_os_** modules, to handle exit and clearing the terminal functions, **_csv_** for all file related actions, **_time_** for some of the wait that was implemented so that the user had enough time to read the messages printed on the terminal before that screen cleared and the next one came up, **_re_**, as was mentioned above, to validate names and **_argparse_** to validate arguments.

### Packages that need to be installed with pip
There is only one package that was needed to be installed which is call **_tabulate_** and it was added to the [requirements.txt](/requirements.txt) file. The use of this module is to present the list of tasks in a nicer and better looking way. Other packages were used such as **_pytest_** that also required installation, but those were not needed for the main project but for the unit testing carried out in [test_project.py](/test_project.py).

## A CLASS JUST FOR THIS APP
In order to handle the tasks in a way that allows for escalability a new class was created with setters, getters, an init method and a way of printing the task information. This, done at the beginning of the project, made it so much easier to add other properties such as the unique id when they were required later on.

## CREATING THE DOCUMENTATION
As part of the developing of this app, special care was put into documenting every function, method, their parameters and their returns. Docstrings were used throughout and the numpy notation system was checked so that it could be used to denote the parameters, their type and the returns of functions. That allowed for a quick documentations created in the [docs](/docs/) folder using a module that was installed using pip called **_pdoc_** which generates an automated html documentation file.

## FURTHER DEVELOPMENT 
A project would never be finished, especially one done without hard deadlines or external requirements, because there is always something else to add or to improve or to make more efficient. So there comes a point when, even though one could think of a dozen things still to do or to add in order to improve the app, one has to decide to stop working on it and hand the project in. If, in the future, I continue to work on it (and I might, since this was a fantastic learning experience, and it could carry on being that, beyond CS50), one question may be asked. What would I do with it? What would I change? What would I add? What would be the direction of further development? That is he purpose of this section, to discuss where I would envision this application going.

First of all, there is one annoying thing about the user experience in this app. All of the actions of creating a new task, modifying an existing one or removing one are cumbersome to some point, especially when doing a lot at once. Many times I found myself wishing I could type "remove" and the id number of the task directly, rather than having to type "remove", let the app load that screen and be prompted for the id and then type in that. The same goes for modifying a task. Wouldn't it be nice to type "modify" the id and the new priority? The same thing could be said for creating new tasks. It would be ideal to be able to either do it in a new screen or typing "new description priority" and let that sort it out and create it.

That would require further refactoring the functions to make use of the common code between the function that gets activated by accept_command() and a function that sends all the user input to that function. It would also required to be able to distinguis between the simplest input allowed at the moment by the switch statement and the matching that the **_re_** module would allow the app to do in order to extract the information that would be needed to implement this functionality.

Some other things that this project could further do is to limit the number of tasks that can be added, since there are no limits at the moment, to add other parameters to the tasks, like a first action step, to add a focus mode to select a task and then bring up the next steps to do it, to name a few.