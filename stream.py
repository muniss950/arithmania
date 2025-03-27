
import streamlit as st
import mysql.connector
import datetime

# MySQL Connection
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="12345",
#     database="math_tutor"
# )
#
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="math_tutor",
    charset="utf8mb4",
    collation="utf8mb4_general_ci"
)
cursor = conn.cursor()

st.title("📚 Math Tutor - Performance Tracker")

# Fetch Students
cursor.execute("SELECT student_id, name FROM students")
students = cursor.fetchall()
student_dict = {id: name for id, name in students}

# Select Student
student_id = st.selectbox("Select Student", list(student_dict.keys()), format_func=lambda x: student_dict[x])

# Input Math Question
question = st.text_input("Enter Math Question (LaTeX Supported)")
correct_answer = st.text_input("Enter Correct Answer")
student_answer = st.text_input("Enter Student's Answer")

# Submit Answer
if st.button("Submit Answer"):
    score = 1.0 if student_answer.strip() == correct_answer.strip() else 0.0  # Simple comparison
    cursor.execute("INSERT INTO performance (student_id, question, student_answer, correct_answer, score) VALUES (%s, %s, %s, %s, %s)",
                   (student_id, question, student_answer, correct_answer, score))
    conn.commit()
    st.success("Answer Submitted!")

# Show Performance History
st.subheader("📊 Student Performance")
cursor.execute("SELECT question, student_answer, correct_answer, score, timestamp FROM performance WHERE student_id = %s ORDER BY timestamp DESC", (student_id,))
results = cursor.fetchall()

for row in results:
    question, student_ans, correct_ans, score, timestamp = row
    st.write(f"**📝 Question:** {question}")
    st.write(f"✅ **Correct Answer:** {correct_ans}")
    st.write(f"❓ **Student's Answer:** {student_ans}")
    st.write(f"📊 **Score:** {score} | 🕒 {timestamp}")
    st.markdown("---")

conn.close()
