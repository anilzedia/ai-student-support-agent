import streamlit as st
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI Student Support Agent", layout="wide")

st.title("🎓 AI Student Support Agent")
st.write("Ask questions related to ERP, examinations, fees, hall tickets, and registrations.")

student_id = st.text_input("Enter Student ID")
query = st.text_area("Ask your question")

if st.button("Get Response"):

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    student = cursor.fetchone()

    if student:
        context = f'''
        Student Name: {student[1]}
        Student ID: {student[2]}
        CGPA: {student[3]}
        Fee Status: {student[4]}
        Hall Ticket: {student[5]}
        Backlog Courses: {student[6]}
        '''

        prompt = f'''
        You are a professional ERP and examination support assistant.

        Student Details:
        {context}

        User Query:
        {query}

        Provide a helpful professional response.
        '''

        response = model.generate_content(prompt)

        st.success(response.text)

    else:
        st.error("Student not found")