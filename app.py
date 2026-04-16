# app.py
import streamlit as st
import mysql.connector

# DB CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="chat_system"
) 
cursor = conn.cursor()

st.title("💬 Chat System")

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Users", "Messages"])

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.header("📊 Dashboard")

    cursor.execute("SELECT COUNT(*) FROM users")
    st.write("Total Users:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM messages")
    st.write("Total Messages:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM messages WHERE message_status='Read'")
    st.write("Read Messages:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM users WHERE status='Online'")
    st.write("Online Users:", cursor.fetchone()[0])

    cursor.execute("SELECT file_type, COUNT(*) FROM attachments GROUP BY file_type")
    st.write("Attachments by Type:")
    st.write(cursor.fetchall())

# ---------------- USERS ----------------
elif menu == "Users":
    st.header("👤 Users")

    if st.button("Show Users"):
        cursor.execute("SELECT * FROM users")
        st.write(cursor.fetchall())

# ---------------- MESSAGES ----------------
elif menu == "Messages":
    st.header("✉️ Messages")

    if st.button("Show Messages"):
        cursor.execute("SELECT * FROM messages")
        st.write(cursor.fetchall())