import streamlit as st
import sqlite3
from datetime import datetime
st.subheader("📊 Advanced Dashboard")

# Total messages
total = cursor.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
st.metric("Total Messages", total)

# Read messages
read = cursor.execute("""
SELECT COUNT(*) FROM messages WHERE message_status='Read'
""").fetchone()[0]
st.metric("Read Messages", read)

# Messages per sender
sender_data = cursor.execute("""
SELECT sender_id, COUNT(*) FROM messages GROUP BY sender_id
""").fetchall()

st.write("Messages per Sender")
st.bar_chart({f"User {s[0]}": s[1] for s in sender_data})

# Messages per receiver
receiver_data = cursor.execute("""
SELECT receiver_id, COUNT(*) 
FROM chats 
GROUP BY receiver_id
""").fetchall()

st.write("Chats per Receiver")
st.bar_chart({f"User {r[0]}": r[1] for r in receiver_data})

# Attachment types (simulate if empty)
attachments = cursor.execute("""
SELECT file_type, COUNT(*) FROM attachments GROUP BY file_type
""").fetchall() if True else []

if attachments:
    st.write("Attachment Types")
    st.bar_chart({a[0]: a[1] for a in attachments})
# ================= DATABASE SETUP =================
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    status TEXT,
    last_seen TEXT
);

CREATE TABLE IF NOT EXISTS chats (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    send_id INTEGER,
    receiver_id INTEGER,
    chat_date TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    sender_id INTEGER,
    message_text TEXT,
    timestamp TEXT,
    message_status TEXT
);
""")
conn.commit()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= AUTH =================
def login(email, password):
    user = cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password)).fetchone()
    return user

# ================= UI =================
st.title("💬 Chat System Pro")

if st.session_state.user is None:
    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    if menu == "Register":
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            try:
                cursor.execute("INSERT INTO user (user_name, email, password, status, last_seen) VALUES (?, ?, ?, 'Online', ?)",
                               (name, email, password, datetime.now()))
                conn.commit()
                st.success("Registered! Now login.")
            except:
                st.error("User already exists")

    elif menu == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

else:
    user = st.session_state.user
    st.sidebar.write(f"👤 {user[1]}")

    menu = st.sidebar.selectbox("Menu", ["Chat", "Dashboard", "Logout"])

    # ================= CHAT =================
    if menu == "Chat":
        st.subheader("💬 Chat Interface")

        users = cursor.execute("SELECT user_id, user_name FROM user WHERE user_id != ?", (user[0],)).fetchall()
        user_dict = {u[1]: u[0] for u in users}

        selected_name = st.selectbox("Select User", list(user_dict.keys()))
        receiver_id = user_dict[selected_name]

        # get chat
        chat = cursor.execute("""
            SELECT chat_id FROM chats
            WHERE (send_id=? AND receiver_id=?) OR (send_id=? AND receiver_id=?)
        """, (user[0], receiver_id, receiver_id, user[0])).fetchone()

        if chat:
            chat_id = chat[0]
        else:
            cursor.execute("INSERT INTO chats (send_id, receiver_id, chat_date) VALUES (?, ?, ?)",
                           (user[0], receiver_id, datetime.now()))
            conn.commit()
            chat_id = cursor.lastrowid

        # show messages
        messages = cursor.execute("SELECT sender_id, message_text, timestamp FROM messages WHERE chat_id=? ORDER BY timestamp",
                                  (chat_id,)).fetchall()

        for msg in messages:
            if msg[0] == user[0]:
                st.markdown(f"**You:** {msg[1]}")
            else:
                st.markdown(f"**{selected_name}:** {msg[1]}")

        # send message
        new_msg = st.text_input("Type message")
        if st.button("Send"):
            cursor.execute("INSERT INTO messages (chat_id, sender_id, message_text, timestamp, message_status) VALUES (?, ?, ?, ?, 'Sent')",
                           (chat_id, user[0], new_msg, datetime.now()))
            conn.commit()
            st.rerun()

    # ================= DASHBOARD =================
    elif menu == "Dashboard":
        st.subheader("📊 Dashboard")

        total = cursor.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        st.metric("Total Messages", total)

        data = cursor.execute("SELECT sender_id, COUNT(*) FROM messages GROUP BY sender_id").fetchall()

        chart_data = {f"User {d[0]}": d[1] for d in data}
        st.bar_chart(chart_data)

    # ================= LOGOUT =================
    elif menu == "Logout":
        st.session_state.user = None
        st.rerun()
