-- ==============================
-- 1. DATABASE
-- ==============================
CREATE DATABASE ChatSystem;
USE ChatSystem;

-- ==============================
-- 2. TABLES (WITH RELATIONSHIPS)
-- ==============================

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(50),
    status VARCHAR(20),
    last_seen DATETIME
);

CREATE TABLE chatrooms (
    room_id INT PRIMARY KEY,
    room_name VARCHAR(50)
);

CREATE TABLE chats (
    chat_id INT PRIMARY KEY,
    send_id INT,
    receiver_id INT,
    chat_date DATE,
    FOREIGN KEY (send_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);

CREATE TABLE messages (
    message_id INT PRIMARY KEY,
    chat_id INT,
    sender_id INT,
    message_text VARCHAR(255),
    timestamp DATETIME,
    message_status VARCHAR(20),
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
);

CREATE TABLE groupmembers (
    room_id INT,
    user_id INT,
    PRIMARY KEY (room_id, user_id),
    FOREIGN KEY (room_id) REFERENCES chatrooms(room_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE attachments (
    attachment_id INT PRIMARY KEY,
    message_id INT,
    file_name VARCHAR(100),
    file_type VARCHAR(20),
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);

-- ==============================
-- 3. INSERT DATA
-- ==============================

-- USERS
INSERT INTO users VALUES
(1,'Ali Khan','ali@gmail.com','ali123','Online','2026-04-14 09:15:00'),
(2,'Sara Ahmed','sara@gmail.com','sara123','Offline','2026-04-14 08:50:00'),
(3,'Ahmed Raza','ahmed@gmail.com','ahmed123','Away','2026-04-14 09:00:00'),
(4,'Ayesha Noor','ayesha@gmail.com','ayesha123','Online','2026-04-14 09:10:00'),
(5,'Bilal Hussain','bilal@gmail.com','bilal123','Offline','2026-04-13 22:30:00');

-- CHATROOMS
INSERT INTO chatrooms VALUES
(1,'Computer Science'),
(2,'Project Team'),
(3,'Friends Group');

-- CHATS
INSERT INTO chats VALUES
(1,1,2,'2026-04-14'),
(2,2,1,'2026-04-14'),
(3,3,4,'2026-04-14'),
(4,4,5,'2026-04-13'),
(5,1,5,'2026-04-13');

-- MESSAGES
INSERT INTO messages VALUES
(1,1,1,'Hi Sara!','2026-04-14 09:00:00','Read'),
(2,1,2,'Hello Ali!','2026-04-14 09:01:00','Read'),
(3,1,1,'How are you?','2026-04-14 09:02:00','Delivered'),
(4,3,3,'Hi Ayesha!','2026-04-14 08:45:00','Read'),
(5,3,4,'Hello Ahmed!','2026-04-14 08:46:00','Sent'),
(6,4,4,'Are you free?','2026-04-13 19:30:00','Delivered'),
(7,4,5,'Yes, tell me.','2026-04-13 19:32:00','Read'),
(8,5,1,'Hi Bilal!','2026-04-13 21:00:00','Delivered'),
(9,5,5,'Hello Ali!','2026-04-13 21:02:00','Read'),
(10,2,2,'See you soon.','2026-04-14 10:00:00','Sent');

-- GROUP MEMBERS
INSERT INTO groupmembers VALUES
(1,1),
(1,2),
(1,3),
(2,2),
(2,4),
(3,1),
(3,4),
(3,5);

-- ATTACHMENTS
INSERT INTO attachments VALUES
(1,3,'assignment.pdf','PDF'),
(2,6,'schedule.docx','DOCX'),
(3,7,'image.jpg','JPG'),
(4,8,'notes.txt','TXT'),
(5,9,'presentation.pptx','PPTX');