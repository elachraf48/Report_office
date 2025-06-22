from typing import List

class Repository:
    def __init__(self):
        self.tasks = {
            "1": "Open Inbox",
            "2": "Report Not No Junc",
            "3": "Add to Whitelist",
            "4": "Delete All",
            "5": "Delete + Number of Emails",
            "6": "Read Random + Number of Emails"
        }

    def display_tasks(self) -> None:
        print("Select a task:")
        for key, value in self.tasks.items():
            print(f"{key}: {value}")

    def execute_task(self, task_number: str) -> None:
        if task_number in self.tasks:
            task_method = getattr(self, f"task_{task_number}", None)
            if task_method:
                task_method()
            else:
                print("Invalid task selection.")
        else:
            print("Invalid task number.")

    def task_1(self) -> None:
        print("Opening Inbox...")

    def task_2(self) -> None:
        print("Reporting Not No Junc...")

    def task_3(self) -> None:
        print("Adding to Whitelist...")

    def task_4(self) -> None:
        print("Deleting All...")

    def task_5(self) -> None:
        print("Deleting + Number of Emails...")

    def task_6(self) -> None:
        print("Reading Random + Number of Emails...")

def start_repository():
    print("Available tasks:")
    print("1 - Open Inbox")
    print("2 - Report Not No Junc")
    print("3 - Add to Whitelist")
    print("4 - Delete All")
    print("5 - Delete + Number of Emails")
    print("6 - Read Random + Number of Emails")

    tasks = input("Select tasks (use + to select multiple): ").split("+")
    print(f"Selected tasks: {tasks}")

    # Implement task handling logic here
    for task in tasks:
        print(f"Executing task {task}...")