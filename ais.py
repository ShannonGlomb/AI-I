import requests
import os
import time
from datetime import datetime
from collections import defaultdict

# In-memory storage for tasks and context
tasks = []
context = defaultdict(str)

# Helper function to save tasks to a file
def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)

# Helper function to load tasks from a file
def load_tasks():
    global tasks
    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

# Add a new task
def add_task(description, priority=1):
    task = {
        'description': description,
        'priority': priority,
        'created_at': datetime.now().isoformat(),
        'reminder': None
    }
    tasks.append(task)
    save_tasks()
    print("Task added.")

# List all tasks
def list_tasks():
    if not tasks:
        print("No tasks found.")
    for i, task in enumerate(tasks, 1):
        reminder = task['reminder'] if task['reminder'] else "No reminder"
        print(f"{i}. {task['description']} (Priority: {task['priority']}, Reminder: {reminder})")

# Set a reminder for a task
def set_reminder(task_index, minutes_from_now):
    if 0 < task_index <= len(tasks):
        reminder_time = datetime.now() + timedelta(minutes=minutes_from_now)
        tasks[task_index-1]['reminder'] = reminder_time.isoformat()
        save_tasks()
        print(f"Reminder set for {reminder_time}.")
    else:
        print("Invalid task index.")

# Edit an existing task
def edit_task(task_index, new_description=None, new_priority=None):
    if 0 < task_index <= len(tasks):
        if new_description is not None:
            tasks[task_index-1]['description'] = new_description
        if new_priority is not None:
            tasks[task_index-1]['priority'] = new_priority
        save_tasks()
        print("Task updated.")
        # Display updated task
        updated_task = tasks[task_index-1]
        reminder = updated_task['reminder'] if updated_task['reminder'] else "No reminder"
        print(f"Updated Task: {task_index}. {updated_task['description']} (Priority: {updated_task['priority']}, Reminder: {reminder})")
    else:
        print("Invalid task index.")

# Auto-update script from GitHub
def update_script_from_github():
    url = "https://raw.githubusercontent.com/ShannonGlomb/AI-I/main/ais.py"  # Your raw URL
    response = requests.get(url)
    if response.status_code == 200:
        # Create a backup directory if it doesn't exist
        backup_dir = 'script_backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Save the current script as a backup
        backup_filename = f'{backup_dir}/ais_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
        with open(backup_filename, 'w') as file:
            file.write(open(__file__).read())
        
        # Save the updated script
        with open(__file__, 'w') as file:
            file.write(response.text)
        
        print("Script updated successfully. Restarting...")
        # Restart the script
        import os
        import sys
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        print("Failed to download the updated script.")

# Check for updates in the background
def auto_update_check():
    while True:
        # Check for updates every hour (3600 seconds)
        time.sleep(3600)
        print("Checking for script updates...")
        update_script_from_github()

# Main function
def main():
    # Start background update check
    import threading
    update_thread = threading.Thread(target=auto_update_check, daemon=True)
    update_thread.start()

    # Load tasks
    load_tasks()
    
    # Main menu and logic for the script
    print("Welcome to your AI Assistant.")
    while True:
        print("\nChoose an option:")
        print("1. Add task")
        print("2. List tasks")
        print("3. Set reminder")
        print("4. Edit task")
        print("5. Update script")
        print("6. Exit")
        user_input = input("Your choice: ")

        if user_input == '1':
            description = input("Enter task description: ")
            priority = int(input("Enter task priority (1-5): "))
            add_task(description, priority)
        elif user_input == '2':
            list_tasks()
        elif user_input == '3':
            task_index = int(input("Enter task index: "))
            minutes_from_now = int(input("Enter reminder time in minutes: "))
            set_reminder(task_index, minutes_from_now)
        elif user_input == '4':
            task_index = int(input("Enter task index: "))
            new_description = input("Enter new description (leave blank to keep unchanged): ")
            new_priority = input("Enter new priority (leave blank to keep unchanged): ")
            new_priority = int(new_priority) if new_priority else None
            edit_task(task_index, new_description, new_priority)
        elif user_input == '5':
            update_script_from_github()
        elif user_input == '6':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
