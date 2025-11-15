"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
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
    credits INTEGER,
    isPremium BOOLEAN
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

from rxconfig import config

class User:
    def __init__(self, id, name, credits, isPremium):
        self.id : int = id
        self.name : str = name
        self.credits : int = credits
        self.isPremium : bool = isPremium
    
    def _changePremium(self, state): # function only for the User class that sets current user's premium status to what it should be
        if self.id: # Handle potential non-existing users
            self.isPremium = state
        else:
            print(f'Placeholder Error - User {self.id} does not exist') # Add functionality to check if the user's id actually exists later on

    def _changeCredits(self, new_credits): # Potential to add more parameters to handle HOW credits should be changed for respective user
        if self.id: # Handle potential non-existing users
            self.credits = new_credits # Calculating what credits should be set to, to be in other function
        else:
            print(f'Placeholder Error - User {self.id} does not exist') # Add functionality to check if the user's id actually exists later on


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
