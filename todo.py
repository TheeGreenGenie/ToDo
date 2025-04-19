import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, file_path="todo_data.json"):
        
        if not os.path.isabs(file_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.file_path = os.path.join(script_dir, file_path)
        else:
            self.file_path = file_path
        
        print(f"Using data file: {self.file_path}")
        self.tasks = self._load_tasks()
        if self.tasks is None or not isinstance(self.tasks, dict) or "tasks" not in self.tasks:
            self.tasks = {"tasks": []}

    def _load_tasks(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
                    if not isinstance(data, dict) or "tasks" not in data:
                        print(f"Warning, data file '{self.file_path}' has incorrect format. Creating new task list")
                        return {"tasks": []}
                    return data
            except json.JSONDecodeError as e:
                print(f"Erro reading task file: {e}")
                print(f"Creating new task list")
                return {"tasks": []}
            except Exception as e:
                print(f"Unexpected error loading tasks")
                print(f"Creating new task list.")
                return {"tasks" : []}
        else:
            print(f"Task file '{self.file_path}' not found. Creating new file.")

    def _save_tasks(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, description):
        task = {
            "id": len(self.tasks["tasks"]) + 1,
            "description": description,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d- %H:%M:%S"),
            "completed_at": None
        }
        self.tasks["tasks"].append(task)
        self._save_tasks()
        print(f"Task added: {description}")

    def list_tasks(self, show_completed=False):
        if not self.tasks['tasks']:
            print("No tasks found.")
            return
        
        print("\n" + "="*50)
        title = "COMPLETED TASKS" if show_completed else "PENDING TASKS"
        print(f"{title:^50}")
        print('='*50)

        found = False
        for task in self.tasks["tasks"]:
            if task["completed"] == show_completed:
                found = True
                status = "✓" if task['completed'] else "❌"
                print(f"{task['id']:3}. [{status}] {task['description']}")
                if show_completed and task["completed_at"]:
                    print(f"        Completed on: {task['completed_at']}")
        
        if not found:
            status_text = "completed" if show_completed else "pending"
            print(f"No {status_text} tasks found.")
        print('='*50 + '\n')

    def complete_task(self, task_id):
        for task in self.tasks['tasks']:
            if task['id'] == task_id:
                if task["completed"]:
                    print(f"Task {task_id} is alrady marked as completed.")
                else:
                    task['completed'] = True
                    task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._save_tasks()
                    print(f"Task {task_id}")
                return
        print(f"task with ID {task_id} not found.")

    def delete_task(self, task_id):
        initial_length = len(self.tasks['tasks'])
        self.tasks['tasks'] = [task for task in self.tasks['tasks'] if task['id'] != task_id]

        if len(self.tasks['tasks']) < initial_length:
            for i, task in enumerate(self.tasks['tasks']):
                task['id'] = i + 1

            self._save_tasks()
            print(f"Task {task_id} has been deleted.")
        else:
            print(f"Task with ID {task_id} not found.")

def print_help():
    print("\n==== TO-DO LIST HELP ====")
    print("Available commands:")
    print("  add <task>     - Add a new task")
    print("  list           - List all pending tasks")
    print("  completed      - List all completed tasks")
    print("  complete <id>  - Mark a task as completed")
    print("  delete <id>    - Delete a task")
    print("  help           - Show this help menu")
    print("  exit           - Exit the program")
    print("=======================\n")

def main():
    todo_list = TodoList()

    print("\nWelcome to the To-Do list Application")
    print_help()

    while True:
        command = input("\nEnter a command: ").strip()

        if command.lower() == 'exit':
            print('Goodbye')
            break

        elif command.lower() == 'help':
            print_help()

        elif command.lower() == 'list':
            todo_list.list_tasks(show_completed=False)

        elif command.lower() == 'completed':
            todo_list.list_tasks(show_completed=True)

        elif command.lower().startswith("add "):
            task = command[4:].strip()
            if task:
                todo_list.add_task(task)
            else:
                print("Error: Task description cannot be empty.")
        
        elif command.lower().startswith('complete '):
            try:
                task_id = int(command[9:].strip())
                todo_list.complete_task(task_id)
            except ValueError:
                print("Error: Task ID must be a number")

        elif command.lower().startswith('delete '):
            try:
                task_id = int(command[9:].strip())
                todo_list.complete_task(task_id)
            except ValueError:
                print("Error: Task ID must be a number")

        else:
            print("Unkown command. Type 'help' to see availale commands")

if __name__ == "__main__":
    main()