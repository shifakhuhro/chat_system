import streamlit as st
import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

st.title("💬 Chat System Project")

menu = st.sidebar.selectbox(
    "Menu",
    ["Insert Message", "View Messages", "Update Message", "Delete Message", "Dashboard"]
)

# ================= INSERT =================
if menu == "Insert Message":
    sender = st.text_input("Sender")
    receiver = st.text_input("Receiver")
    message = st.text_area("Message")

    if st.button("Send"):
        cursor.execute("""
        INSERT INTO messages (chat_id, sender_id, message_text, timestamp, message_status)
        VALUES (1, ?, ?, datetime('now'), 'Sent')
        """, (sender, message))
        conn.commit()
        st.success("Message Sent!")

# ================= VIEW =================
elif menu == "View Messages":
    st.subheader("All Messages")

    data = cursor.execute("SELECT * FROM messages").fetchall()
    for row in data:
        st.write(row)

# ================= UPDATE =================
elif menu == "Update Message":
    msg_id = st.number_input("Message ID", min_value=1)
    new_msg = st.text_area("New Message")

    if st.button("Update"):
        cursor.execute("UPDATE messages SET message_text=? WHERE message_id=?",
                       (new_msg, msg_id))
        conn.commit()
        st.success("Updated!")

# ================= DELETE =================
elif menu == "Delete Message":
    msg_id = st.number_input("Message ID", min_value=1)

    if st.button("Delete"):
        cursor.execute("DELETE FROM messages WHERE message_id=?",
                       (msg_id,))
        conn.commit()
        st.warning("Deleted!")

# ================= DASHBOARD =================
elif menu == "Dashboard":
    st.subheader("📊 User Stats")

    stats = cursor.execute("""
        SELECT sender_id, COUNT(*) FROM messages
        GROUP BY sender_id
    """).fetchall()

    for s in stats:
        st.write(f"User {s[0]} sent {s[1]} messages")
