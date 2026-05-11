import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Student Support Agent",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("🎓 AI Student Support Agent")

st.markdown(
    "AI-powered ERP and Examination Support System"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

menu = st.sidebar.selectbox(
    "Navigation",
    ["Student Support", "Dashboard Analytics"]
)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

conn = sqlite3.connect('students.db')

# -----------------------------------
# STUDENT SUPPORT PAGE
# -----------------------------------

if menu == "Student Support":

    st.subheader("🤖 Ask ERP & Examination Queries")

    student_id = st.text_input(
        "Enter Student ID"
    )

    query = st.text_area(
        "Ask your question",
        placeholder="Example: Is my hall ticket generated?"
    )

    if st.button("Get Response"):

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id,)
        )

        student = cursor.fetchone()

        if student:

            name = student[1]
            cgpa = student[3]
            fee_status = student[4]
            hall_ticket = student[5]
            backlog = student[6]
            registered_courses = student[7]
            exam_center = student[8]

            query_lower = query.lower()

            response = ""

            # -----------------------------------
            # AI LOGIC
            # -----------------------------------

            if "hall ticket" in query_lower:

                response = f"""
                Hello {name},

                Your hall ticket status is: {hall_ticket}.

                Please download it from the ERP portal before examination.
                """

            elif "fee" in query_lower:

                response = f"""
                Hello {name},

                Your current fee payment status is: {fee_status}.
                """

            elif "cgpa" in query_lower:

                response = f"""
                Hello {name},

                Your current CGPA is {cgpa}.
                """

            elif "backlog" in query_lower:

                response = f"""
                Hello {name},

                You currently have {backlog} backlog course(s).
                """

            elif "project" in query_lower:

                if cgpa >= 5.5 and backlog == 0:

                    response = f"""
                    Hello {name},

                    You are eligible for Project Work registration.

                    Your CGPA criteria is satisfied.
                    """

                else:

                    response = f"""
                    Hello {name},

                    You are currently not eligible for Project Work.

                    Minimum requirements:
                    - CGPA >= 5.5
                    - No backlog courses

                    Your CGPA: {cgpa}
                    Backlogs: {backlog}
                    """

            elif "exam center" in query_lower:

                response = f"""
                Hello {name},

                Your allocated examination center is:
                {exam_center}
                """

            elif "registration" in query_lower:

                response = f"""
                Hello {name},

                You are currently registered for
                {registered_courses} courses.
                """

            else:

                response = f"""
                Hello {name},

                Your query has been received successfully.

                Please contact ERP support team for additional assistance.
                """

            st.success(response)

        else:

            st.error("Student not found")

# -----------------------------------
# DASHBOARD PAGE
# -----------------------------------

elif menu == "Dashboard Analytics":

    st.subheader("📊 Student Analytics Dashboard")

    df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    # Display Data
    st.dataframe(df)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Students",
            len(df)
        )

    with col2:

        paid_students = len(
            df[df['fee_status'] == 'Paid']
        )

        st.metric(
            "Fee Paid",
            paid_students
        )

    with col3:

        avg_cgpa = round(
            df['cgpa'].mean(),
            2
        )

        st.metric(
            "Average CGPA",
            avg_cgpa
        )

    with col4:

        total_backlogs = df['backlog_courses'].sum()

        st.metric(
            "Total Backlogs",
            total_backlogs
        )

    # Charts

    st.subheader("📈 CGPA Distribution")

    st.bar_chart(df['cgpa'])

    st.subheader("📚 Backlog Analysis")

    st.bar_chart(df['backlog_courses'])

    st.subheader("💰 Fee Status")

    fee_counts = df['fee_status'].value_counts()

    st.bar_chart(fee_counts)

    st.subheader("🏢 Exam Center Distribution")

    exam_counts = df['exam_center'].value_counts()

    st.bar_chart(exam_counts)

# -----------------------------------
# CLOSE CONNECTION
# -----------------------------------

conn.close()