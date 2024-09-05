import sqlite3
import streamlit as st

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

# Create a table for the to-do list if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pending'
                 )''')

# Function to add a task
def add_task(task):
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()

# Function to view all tasks
def view_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    return tasks

# Function to update a task's status
def update_task(task_id, status):
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()

# Function to delete a task
def delete_task(task_id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()

# Streamlit App Interface
st.title("To-Do List Application")

# Initialize session state for task input and refresh flag
if 'task_input' not in st.session_state:
    st.session_state.task_input = ""

if 'refresh' not in st.session_state:
    st.session_state.refresh = False

# Input section for adding a new task
st.header("Add a New Task")
new_task = st.text_input("Task Name", value=st.session_state.task_input)
if st.button("Add Task"):
    if new_task:
        add_task(new_task)
        st.session_state.task_input = ""  # Clear the input field
        st.session_state.refresh = True    # Set refresh flag
    else:
        st.error("Task name cannot be empty.")

# Display all tasks
st.header("Current Tasks")
tasks = view_tasks()

if tasks:
    for task in tasks:
        col1, col2, col3, col4 = st.columns([1, 4, 2, 1])
        col1.write(task[0])
        col2.write(task[1])
        col3.write(task[2])
        
        if col4.button("Delete", key=f"delete_{task[0]}"):
            delete_task(task[0])
            st.session_state.refresh = True  # Set refresh flag

else:
    st.write("No tasks found.")

# Update task status
st.header("Update Task Status")
task_id_to_update = st.number_input("Enter Task ID to Update", min_value=1, step=1)
new_status = st.selectbox("New Status", ["Pending", "Completed"])

if st.button("Update Status"):
    update_task(task_id_to_update, new_status)
    st.session_state.refresh = True  # Set refresh flag

# Check if refresh is needed
if st.session_state.refresh:
    st.session_state.refresh = False  # Reset the refresh flag
    st.rerun()  # Use this line to ensure the interface reflects the updates

# Close the connection when done
conn.close()
