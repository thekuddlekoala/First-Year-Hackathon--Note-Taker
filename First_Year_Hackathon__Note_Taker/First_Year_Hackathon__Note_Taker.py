"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import sqlite3
import bcrypt
import re
from datetime import datetime

# ============================================================
# DATABASE CONFIG (YOUR EXISTING NotesDB SETUP)
# ============================================================

conn = sqlite3.connect("NotesDB")
cursor = conn.cursor()
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
    DOB TEXT NOT NULL,  -- store as 'DD-MM-YYYY'
    profile_picture TEXT,
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
    date_of_creation TEXT NOT NULL,
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

conn.commit()
conn.close()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def email_exists(email: str) -> bool:
    conn = sqlite3.connect("NotesDB")
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def add_user(name: str, email: str, password: str, dob: str):
    conn = sqlite3.connect("NotesDB")
    cur = conn.cursor()

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cur.execute("""
        INSERT INTO users (name, email, password, credits, isPremium, DOB)
        VALUES (?, ?, ?, 0, 0, ?)
    """, (name, email, hashed_pw, dob))

    conn.commit()
    conn.close()


# ============================================================
# STATE (ALL LOGIN + SIGNUP LOGIC IN ONE PLACE)
# ============================================================

class State(rx.State):
    """The app state."""

def landingPage() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to Note Taker!", font_size="2", mb="2", align="center"),
        rx.vstack(
            rx.link("Login", href="/login", style={"textDecoration": "none"}),
            rx.link("Sign Up", href="/signup", style={"textDecoration": "none"}),
            spacing="1"
        ),
        align_items="center",
        justify_content="center",
        height="100vh",
    )


def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Login", size="6", mb="4"),

            # EMAIL
            rx.vstack(
                rx.input(
                    placeholder="Email",
                    value=State.login_email,
                    on_change=State.on_email_change,
                    width="80",
                ),
                rx.cond(
                    State.login_email_error != "",
                    rx.text(State.login_email_error, color="red", font_size="0.8rem")
                ),
                spacing="1",
                width="80",
            ),

            # PASSWORD
            rx.vstack(
                rx.input(
                    placeholder="Password",
                    type="password",
                    value=State.login_password,
                    on_change=State.on_password_change,
                    width="80",
                ),
                rx.cond(
                    State.login_password_error != "",
                    rx.text(State.login_password_error, color="red", font_size="0.8rem")
                ),
                spacing="1",
                width="80",
            ),

            rx.button("Login", width="80", mt="2"),
            spacing="2",
        ),
        height="100vh",
    )


def signup_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Create Account", size="6"),

            rx.input(
                placeholder="Email",
                value=State.email,
                on_change=State.set_email,
                width="300px",
            ),
            rx.input(
                placeholder="Full Name",
                value=State.name,
                on_change=State.set_name,
                width="300px",
            ),
            rx.input(
                type="date",
                value=State.dob,
                on_change=State.set_dob,
                width="300px",
            ),
            rx.input(
                placeholder="Password",
                type="password",
                value=State.password,
                on_change=State.set_password,
                width="300px",
            ),

            rx.button("Sign Up", on_click=State.submit, width="200px"),

            rx.text(State.message, color=State.message_color, weight="bold", margin_top="10px"),

            spacing="4",
            padding="20px",
        )
    )


# ============================================================
# APP SETUP
# ============================================================

app = rx.App()
app.add_page(landingPage, route="/")
app.add_page(login_page, route="/login")
