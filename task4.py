tasks = {
    "task1": "Виконано",
    "task2": "Виконано",
    "task3": "Виконано",
    "task4": "В процесі",
    "task5": "Очікує"
}
def add_task(task_name, status="Очікує"):

    if task_name in tasks:
        print(f"Задача '{task_name}' вже існує.")
    else:
        tasks[task_name] = status
        print(f"Задача '{task_name}' додана зі статусом '{status}'.")

def remove_task(task_name):

    if task_name in tasks:
        del tasks[task_name]
        print(f"Задача '{task_name}' видалена.")
    else:
        print(f"Задача '{task_name}' не знайдена.")

def update_task_status(task_name, new_status):

    if task_name in tasks:
        tasks[task_name] = new_status
        print(f"Статус задачі '{task_name}' оновлено до '{new_status}'.")
    else:
        print(f"Задача '{task_name}' не знайдена.")

def get_pending_tasks():
    #список задач з статусом очікує
    pending = [task for task, status in tasks.items() if status == "Очікує"]
    return pending

add_task("task6")
remove_task("task3")
update_task_status("task4", "Виконано")
print("Задачі, що очікують виконання:", get_pending_tasks())