import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

# AUTO CREATE TABLES (IMPORTANT FOR DEPLOYMENT)
cursor.executescript("""
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT,
    email TEXT,
    password TEXT,
    status TEXT,
    last_seen TEXT
);

CREATE TABLE IF NOT EXISTS chats (
    chat_id INTEGER PRIMARY KEY,
    send_id INTEGER,
    receiver_id INTEGER,
    chat_date TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY,
    chat_id INTEGER,
    sender_id INTEGER,
    message_text TEXT,
    timestamp TEXT,
    message_status TEXT
);
""")

conn.commit()
import streamlit as st
import sqlite3

# Connect DB
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

st.title("💬 Chat System Project")

menu = st.sidebar.selectbox(
    "Menu",
    ["Insert Message", "View Messages", "Update Message", "Delete Message", "Dashboard"]
)

# ================= INSERT =================
if menu == "Insert Message":
    sender_id = st.number_input("Sender ID", min_value=1)
    receiver_id = st.number_input("Receiver ID", min_value=1)
    message = st.text_area("Message")

    if st.button("Send"):
        # Find chat_id
        chat = cursor.execute("""
            SELECT chat_id FROM chats 
            WHERE send_id=? AND receiver_id=?
        """, (sender_id, receiver_id)).fetchone()

        if chat:
            chat_id = chat[0]
        else:
            # create new chat
            cursor.execute("""
                INSERT INTO chats (send_id, receiver_id, chat_date)
                VALUES (?, ?, date('now'))
            """, (sender_id, receiver_id))
            conn.commit()
            chat_id = cursor.lastrowid

        # Insert message
        cursor.execute("""
            INSERT INTO messages (chat_id, sender_id, message_text, timestamp, message_status)
            VALUES (?, ?, ?, datetime('now'), 'Sent')
        """, (chat_id, sender_id, message))

        conn.commit()
        st.success("Message Sent!")

# ================= VIEW =================
elif menu == "View Messages":
    st.subheader("All Messages")

    data = cursor.execute("""
        SELECT message_id, sender_id, message_text, timestamp, message_status
        FROM messages
    """).fetchall()

    for row in data:
        st.write(row)

# ================= UPDATE =================
elif menu == "Update Message":
    msg_id = st.number_input("Message ID", min_value=1)
    new_msg = st.text_area("New Message")

    if st.button("Update"):
        cursor.execute("""
            UPDATE messages 
            SET message_text=?, message_status='Read'
            WHERE message_id=?
        """, (new_msg, msg_id))
        conn.commit()
        st.success("Updated!")

# ================= DELETE =================
elif menu == "Delete Message":
    msg_id = st.number_input("Message ID", min_value=1)

    if st.button("Delete"):
        cursor.execute("DELETE FROM messages WHERE message_id=?", (msg_id,))
        conn.commit()
        st.warning("Deleted!")

# ================= DASHBOARD =================
elif menu == "Dashboard":
    st.subheader("📊 Dashboard")

    # Total messages
    total = cursor.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    st.write(f"Total Messages: {total}")

    # Messages per user
    stats = cursor.execute("""
        SELECT sender_id, COUNT(*) 
        FROM messages
        GROUP BY sender_id
    """).fetchall()

    st.write("Messages per user:")
    for s in stats:
        st.write(f"User {s[0]} → {s[1]} messages")

    # Read messages
    read = cursor.execute("""
        SELECT COUNT(*) FROM messages WHERE message_status='Read'
    """).fetchone()[0]

    st.write(f"Read Messages: {read}")
