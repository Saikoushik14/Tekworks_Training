import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import get_connection

st.title("Student Performance Management System")

# ADD STUDENT
st.header("Add Student")

name = st.text_input("Name")
age = st.number_input("Age", min_value=1)
subject = st.text_input("Subject")
marks = st.number_input("Marks", min_value=0, max_value=100)

if st.button("Add Student"):
    if name and subject:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, age, subject, marks) VALUES (%s,%s,%s,%s)",
            (name, age, subject, marks)
        )
        conn.commit()
        conn.close()
        st.success("Student added successfully")
    else:
        st.error("Please fill all fields")

# VIEW STUDENTS
st.header("View Students")

conn = get_connection()
df = pd.read_sql("SELECT * FROM students", conn)
conn.close()

if not df.empty:
    df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    st.dataframe(df)
else:
    st.warning("No student records found")

# UPDATE MARKS
st.header("Update Marks")

student_id = st.number_input("Student ID", min_value=1)
new_marks = st.number_input("New Marks", min_value=0, max_value=100)

if st.button("Update Marks"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET marks=%s WHERE id=%s",
        (new_marks, student_id)
    )
    conn.commit()
    conn.close()
    st.success("Marks updated")

# DELETE STUDENT
st.header("Delete Student")

delete_id = st.number_input("Student ID to Delete", min_value=1)

if st.button("Delete Student"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (delete_id,))
    conn.commit()
    conn.close()
    st.warning("Student record deleted")

# ANALYTICS
st.header("Analytics")

if not df.empty:
    st.metric("Average Marks", round(df["marks"].mean(), 2))

    pass_percentage = (df[df["marks"] >= 40].shape[0] / df.shape[0]) * 100
    st.metric("Pass Percentage", f"{round(pass_percentage,2)}%")

    topper = df.loc[df["marks"].idxmax()]
    st.write("🏆 Top Scorer")
    st.write(topper)

    subject_avg = df.groupby("subject")["marks"].mean()

    # Bar Chart
    st.subheader("Subject-wise Average Marks")
    plt.figure()
    subject_avg.plot(kind="bar")
    plt.ylabel("Average Marks")
    plt.xlabel("Subject")
    st.pyplot(plt)

    # Pie Chart
    st.subheader("Pass / Fail Ratio")
    status_count = df["Status"].value_counts()
    plt.figure()
    plt.pie(status_count, labels=status_count.index, autopct="%1.1f%%")
    st.pyplot(plt)
