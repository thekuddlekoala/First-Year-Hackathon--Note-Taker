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
    credits INTEGER DEFAULT 0,
    isPremium BOOLEAN DEFAULT FALSE,
    DOB TEXT NOT NULL,
    profile_picture TEXT,
    email TEXT NOT NULL UNIQUE
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

    # Login fields
    login_email: str = ""
    login_password: str = ""
    login_email_error: str = ""
    login_password_error: str = ""

    # Signup fields
    email: str = ""
    name: str = ""
    dob: str = ""
    password: str = ""

    message: str = ""
    message_color: str = "red"

    # --------------------
    # LOGIN VALIDATION
    # --------------------
    def on_email_change(self, value: str):
        self.login_email = value
        pattern = r"^(?![.-])[a-zA-Z0-9._%+-]+(?<![.-])@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$"

        if not re.fullmatch(pattern, value):
            self.login_email_error = "Please enter a valid email address."
        else:
            self.login_email_error = ""

    def on_password_change(self, value: str):
        self.login_password = value
        pattern = (r"^(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])"
                   r"(?=.*[a-zA-Z])(?=.*\d).{8,}$")

        if not re.fullmatch(pattern, value):
            self.login_password_error = "Password must be 8+ chars, include a number and symbol."
        else:
            self.login_password_error = ""

    # --------------------
    # SIGNUP VALIDATION
    # --------------------
    def validate_email(self):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.email)

    def validate_password(self):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
        return re.match(pattern, self.password)

    def validate_name(self):
        return len(self.name.strip()) >= 2

    def validate_dob(self):
        try:
            dob_date = datetime.strptime(self.dob, "%Y-%m-%d")
            return dob_date < datetime.now()
        except:
            return False

    # --------------------
    # SIGNUP SUBMIT
    # --------------------
    def submit(self):

        if not self.validate_email():
            self.message = "Invalid email address!"
            return

        if not self.validate_name():
            self.message = "Name must be at least 2 characters!"
            return

        if not self.validate_dob():
            self.message = "Invalid date of birth!"
            return

        if not self.validate_password():
            self.message = (
                "Password must be 8+ chars, include uppercase, lowercase, number & special character."
            )
            return

        if email_exists(self.email):
            self.message = "Email already registered!"
            return

        add_user(self.name, self.email, self.password, self.dob)

        self.message = "Account created successfully!"
        self.message_color = "green"

        # Reset fields
        self.email = ""
        self.name = ""
        self.password = ""
        self.dob = ""


# ============================================================
# PAGES
# ============================================================

def landingPage() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to Note Taker!", font_size="2", mb="2"),
        rx.vstack(
            rx.link("Login", href="/login", style={"textDecoration": "none"}),
            rx.link("Sign Up", href="/signup", style={"textDecoration": "none"}),
            spacing="1",
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
app.add_page(signup_page, route="/signup")
