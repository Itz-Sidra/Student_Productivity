import streamlit as st
import sqlite3
import PyPDF2
from docx import Document
import openai

# Set up OpenAI API key (replace with your own key)
openai.api_key = "your_openai_api_key"

# Database Setup
def setup_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section TEXT NOT NULL,
        task TEXT NOT NULL,
        deadline TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)
    conn.commit()
    conn.close()

# Add Task to Database
def add_task(section, task, deadline):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (section, task, deadline) VALUES (?, ?, ?)", (section, task, deadline))
    conn.commit()
    conn.close()

# Get All Tasks
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return tasks

# Mark Task as Complete
def mark_complete(task_id):
    conn = sqlite3.connect("tasks.db")
    conn.execute("UPDATE tasks SET status = 'Complete' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Extract Notes from PDF
def extract_notes_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    notes = ""
    for page in pdf_reader.pages:
        notes += page.extract_text()
    return notes

# Extract Notes from Word File
def extract_notes_from_docx(file):
    doc = Document(file)
    notes = ""
    for para in doc.paragraphs:
        notes += para.text + "\n"
    return notes

# Chatbot Interaction
def ai_chatbot(query):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer this question conceptually: {query}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit App
st.title("Student Platform")

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["To-Do List", "Notes Generator", "AI Chatbot"])

# Tab 1: To-Do List
with tab1:
    st.header("To-Do List with Sections")

    # Add Task
    section = st.text_input("Section")
    task = st.text_input("Task")
    deadline = st.date_input("Deadline")
    if st.button("Add Task"):
        if section and task:
            add_task(section, task, deadline)
            st.success("Task added successfully!")
        else:
            st.error("Section and Task are required!")

    # Display Tasks
    st.subheader("Tasks")
    tasks = get_tasks()
    for task in tasks:
        st.write(f"**Section:** {task[1]} | **Task:** {task[2]} | **Deadline:** {task[3]} | **Status:** {task[4]}")
        if task[4] == "Pending" and st.button(f"Mark Complete - Task {task[0]}"):
            mark_complete(task[0])
            st.success(f"Task {task[0]} marked as complete!")

# Tab 2: Notes Generator
with tab2:
    st.header("Document Upload and Notes Generation")

    # File Upload
    uploaded_file = st.file_uploader("Upload a document (PDF or Word)", type=["pdf", "docx"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            notes = extract_notes_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            notes = extract_notes_from_docx(uploaded_file)
        else:
            notes = "Unsupported file type."

        # Display Notes
        st.subheader("Generated Notes")
        st.text_area("Notes", notes, height=300)

# Tab 3: AI Chatbot
with tab3:
    st.header("AI Chatbot for Homework Assistance")

    # User Query
    query = st.text_input("Ask a question:")
    if st.button("Get Answer"):
        if query:
            answer = ai_chatbot(query)
            st.subheader("Answer")
            st.write(answer)
        else:
            st.error("Please enter a question!")

# Setup the database on first run
setup_database()
