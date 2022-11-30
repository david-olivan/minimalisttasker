# THE MINIMALIST TASKER
#### Video Demo:  <URL HERE>
#### Description: The purpose of this project is to create a simple terminal application that allows us to create a database for our tasks, either an individual one or one for each project. The app will use the database to load, save and store the tasks which will be added to it, each with a priority level, an automatically generated id and a task description. The app will present these tasks in a table, ordered by priority and allow the user to add new tasks, remove the completed ones and modify either the priority or the description.

# WELCOME TO THE MINIMALIST TASKER

## FEATURES
here are a few things, but ot too many, it's still a minimalist app ;), that The Minimalist Tasker allows us to do. First of all it lets us either launch the application just using "python" and the name of the .py file. Then it ask us for the name of the database we want to use. Alternatively we can write that name as an argument right after the .py filename when laknching the application. Any other combination of arguments or lack thereof will be met with reproach by the handy [name lf module]. Both when giv9ng a database name dorectly or after launching, the app will chechk first if such a name follows the naming rules established in the app. if it doesnt itll let the user now and prompt them for a new name. If the name is valid, however, the app will next check if a database with rhat name exists, kn which case it will load it, or if it doesn't, in which case it'll create it.

### A word on the databases used
As part of the planning process for this project which file system for the database to store the tasks was considered, finally deciding on .csv files for the easiness in which they may be used for information that does not have a lot of volume. SQL-like databases were discarded since they sid not seem to add a lot to a project with few tasks and each task with very few bits of informstion. Thus, the time invrsted in taming a mlre complex file system was deemed more appropristely allocated to the myriad other things that had to be learnt and applied.
If the database had sny tasks stored inside, they will be loaded onto a list made up pf Task objects (a class created for this project) and said list will be ordered and presented to the user by passing it to a dedicated function. Most of the functionally was slowly refactored out of main() and nto their own independent functions and the display_tasks() was one such change.

### What if my newly created databae doesnt have any tasks?
Even though the example.csv file contains a number of tasks as examples of what the app can do, when a user creates a new database it will not be pipulated. That is not a problem, because one of the features is the creation of new tasks. When using this option the tittle st the top of the text within the terminal will change (using a function to maintain the handdrawn box around it) and the app will prompt the user for the name of the task and the priority the user wants to assign to it, checking that the name is not longer than a 100 characters and the prioritt is a nimber between 1 and 5, voth included, and letting the user know when these conditoons have not been met.

## SOME PACKAGES IT USES
## A CLASS JUST FOR THIS APP