"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx

import sqlite3

conn = sqlite3.connect("NotesDB")
cursor = conn.cursor()

#Creating tables
cursor.execute("PRAGMA foreign_keys = ON;")

# ============================
# User Table
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    password TEXT,
    credits INTEGER,
    isPremium BOOLEAN,
    DOB TEXT NOT NULL,  -- store as 'YYYY-MM-DD'
    profile_picture BLOB,
    email TEXT NOT NULL
)
""")

# ============================
# Image Table
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY,
    content BLOB
)
""")

# ============================
# Note Table
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY,
    userid INTEGER,
    upvote INTEGER,
    downvote INTEGER,
    imageid INTEGER,
    date_of_creation TEXT NOT NULL, -- store as 'YYYY-MM-DD'
    tags TEXT,
    visibility TEXT CHECK(visibility IN ('Public', 'Private', 'Shared')),
    academic_level TEXT CHECK(academic_level IN ('GCSE', 'A-Level', 'University')),
    FOREIGN KEY (userid) REFERENCES users(id),
    FOREIGN KEY (imageid) REFERENCES images(id)
)
""")

# ============================
# Note Shared With Table
# ============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS note_shared_with (
    id INTEGER PRIMARY KEY,
    userid INTEGER,
    noteid INTEGER,
    FOREIGN KEY (userid) REFERENCES users(id),
    FOREIGN KEY (noteid) REFERENCES notes(id)
)
""")

# Commit and close
conn.commit()
conn.close()

class State(rx.State):
    """The app state."""

def landingPage() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to Note Taker!", font_size="2em", mb="2em"),
        rx.vstack(
            rx.link("Login", href="/login", style={"textDecoration": "none"}),
            rx.link("Sign Up", href="/signup", style={"textDecoration": "none"}),
            #spacing="1em"
        ),
        align_items="center",
        justify_content="center",
        height="100vh"
    )


app = rx.App()
app.add_page(landingPage, route="/")
