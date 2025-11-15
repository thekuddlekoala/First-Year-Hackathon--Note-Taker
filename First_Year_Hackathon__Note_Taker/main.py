"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
from rxconfig import config

import sqlite3

conn = sqlite3.connect("NotesDB")
cursor = conn.cursor()

#Creating tables
cursor.execute("""
    PRAGMA foreign_keys = ON;

-- ============================
-- User Table
-- ============================
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    password TEXT
    credits INTEGER,
    isPremium BOOLEAN
    DOB date TEXT NOT NULL -- store as 'YYYY-MM-DD'
);

-- ============================
-- Image Table
-- ============================
CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    content BLOB
);

-- ============================
-- Note Table
-- ============================
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    userid INTEGER,
    upvote INTEGER,
    downvote INTEGER,
    imageid INTEGER,
    date_of_creation TEXT NOT NULL -- store as 'YYYY-MM-DD'
    tags TEXT,
    
    -- ENUM visibility = {Public, Private, Shared}
    visibility TEXT CHECK(visibility IN ('Public', 'Private', 'Shared')),
    
    -- ENUM academic_level = {GCSE, A-Level, University}
    academic_level TEXT CHECK(academic_level IN ('GCSE', 'A-Level', 'University')),
    
    FOREIGN KEY (userid) REFERENCES user(id),
    FOREIGN KEY (imageid) REFERENCES image(id)
);

-- ============================
-- Note Shared With Table
-- ============================
CREATE TABLE note_shared_with (
    id INTEGER PRIMARY KEY,
    userid INTEGER,
    noteid INTEGER,
    
    FOREIGN KEY (userid) REFERENCES user(id),
    FOREIGN KEY (noteid) REFERENCES note(id)
);

               
""")

class State(rx.State):
    """The app state."""

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
