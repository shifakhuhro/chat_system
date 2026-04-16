import sqlite3

conn = sqlite3.connect("chat.db")
cursor = conn.cursor()

# ================= USER =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT,
    email TEXT,
    password TEXT,
    status TEXT,
    last_seen TEXT
)
""")

# ================= CHATS =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    chat_id INTEGER PRIMARY KEY,
    send_id INTEGER,
    receiver_id INTEGER,
    chat_date TEXT
)
""")

# ================= MESSAGES =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY,
    chat_id INTEGER,
    sender_id INTEGER,
    message_text TEXT,
    timestamp TEXT,
    message_status TEXT
)
""")

# ================= CHATROOMS =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS chatrooms (
    room_id INTEGER PRIMARY KEY,
    room_name TEXT
)
""")

# ================= GROUP MEMBERS =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS groupmembers (
    room_id INTEGER,
    user_id INTEGER
)
""")

# ================= ATTACHMENTS =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS attachments (
    attachment_id INTEGER PRIMARY KEY,
    message_id INTEGER,
    file_name TEXT,
    file_type TEXT
)
""")

# ================= INSERT DATA =================
cursor.executescript("""
INSERT INTO user VALUES
(1,'Ali Khan','ali@gmail.com','ali123','Online','2026-04-14 09:15'),
(2,'Sara Ahmed','sara@gmail.com','sara123','Offline','2026-04-14 08:50'),
(3,'Ahmed Raza','ahmed@gmail.com','ahmed123','Away','2026-04-14 09:00'),
(4,'Ayesha Noor','ayesha@gmail.com','ayesha123','Online','2026-04-14 09:10'),
(5,'Bilal Hussain','bilal@gmail.com','bilal123','Offline','2026-04-13 22:30');

INSERT INTO chats VALUES
(1,1,2,'2026-04-14'),
(2,2,1,'2026-04-14'),
(3,3,4,'2026-04-14'),
(4,4,5,'2026-04-13'),
(5,1,5,'2026-04-13');

INSERT INTO messages VALUES
(1,1,1,'Hi Sara!','2026-04-14 09:00','Read'),
(2,1,2,'Hello Ali!','2026-04-14 09:01','Read'),
(3,1,1,'How are you?','2026-04-14 09:02','Delivered'),
(4,3,3,'Hi Ayesha!','2026-04-14 08:45','Read'),
(5,3,4,'Hello Ahmed!','2026-04-14 08:46','Sent'),
(6,4,4,'Are you free?','2026-04-13 19:30','Delivered'),
(7,4,5,'Yes, tell me.','2026-04-13 19:32','Read'),
(8,5,1,'Hi Bilal!','2026-04-13 21:00','Delivered'),
(9,5,5,'Hello Ali!','2026-04-13 21:02','Read'),
(10,2,2,'See you soon.','2026-04-14 10:00','Sent');

INSERT INTO chatrooms VALUES
(1,'Computer Science'),
(2,'Project Team'),
(3,'Friends Group');

INSERT INTO groupmembers VALUES
(1,1),(1,2),(1,3),
(2,2),(2,4),
(3,1),(3,4),(3,5);

INSERT INTO attachments VALUES
(1,3,'assignment.pdf','PDF'),
(2,6,'schedule.docx','DOCX'),
(3,7,'image.jpg','JPG'),
(4,8,'notes.txt','TXT'),
(5,9,'presentation.pptx','PPTX');
""")

conn.commit()
conn.close()

print("✅ Database created successfully with correct structure!")