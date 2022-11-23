# 2-11-22
import re, sys, csv

user_input = input("Add task (task - priority): ")
if thingy := re.search(r"^(.*) - ([1-5]?)$" , user_input):
    task, priority = thingy[1], thingy[2]
else:
    sys.exit("The format of the task is not correct.")

print(f"The task is {task} and its priority is {priority}")