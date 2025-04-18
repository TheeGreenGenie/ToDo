import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, file_path="todo_data.json"):
        self.file_path = file_path
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except:
                return {"tasks": []}

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
        pass

    def delete_task(self, task_id):
        pass

    def print_help():
        pass

def main():
    pass

if __name__ == "__main__":
    main()