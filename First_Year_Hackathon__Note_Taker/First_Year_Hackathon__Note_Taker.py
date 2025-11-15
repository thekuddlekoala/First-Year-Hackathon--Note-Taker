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
    username: str = "OnlyTwentyCharacters"
    userIcon: str = "defaultuser.png"

    uploaded_files: list[str] = []
    current_upload_name: str = ""

    @rx.event
    async def setUserIcon(self, iconPath: str):
        self.userIcon = iconPath

    @rx.event
    async def setUsername(self, username: str):
        self.username = username

    @rx.event
    async def getFileName(self) -> str:
        return self.current_upload_name

    @rx.event
    async def setCurrentUploadName(self, name: str):
        self.current_upload_name = name

    @rx.event
    async def handleUpload(
        self, files: list[rx.UploadFile]
    ):
        for file in files:
            data = await file.read()
            path = rx.get_upload_dir() / file.name # type: ignore
            with path.open("wb") as f:
                f.write(data)
            self.uploaded_files = [file.name] # type: ignore

def uploadPage() -> rx.Component:
    return rx.vstack(      
        rx.box(),

        rx.image(
            src=State.userIcon,
            style={"width": "30px", "height": "30px"},
            align = "center",
            position = "relative",
            right = "-48%",
            top = "7px",
        ),

        rx.text(
            State.username,
            style={"width": "100%", "height": "0", "textAlign": "right"},
            align = "center",
            position = "relative",
            right = "4%",
            top = "-30px"
        ),

        
        rx.separator(style={"width": "100%", "height": "1px", "backgroundColor": "#e5e7eb"}),

        rx.heading("Upload Note", font_size="5em", mb="2em", align="center", padding="1em"),
        
        rx.vstack(
            rx.upload.root(
                rx.box(
                    rx.icon(
                        tag="cloud_upload",
                        style={
                            "width": "3rem",
                            "height": "3rem",
                            "color": "#2563eb",
                            "marginBottom": "0.75rem",
                        },
                    ),
                    rx.hstack(
                        rx.text(
                            "Click to upload",
                            style={"fontWeight": "bold", "color": "#1d4ed8"},
                        ),
                        " or drag and drop",
                            style={"fontSize": "0.875rem", "color": "#4b5563"},
                    ),
                    rx.text(
                        "PNG, JPG (MAX. 10MB)",
                        style={"fontSize": "0.75rem", "color": "#6b7280", "marginTop": "0.25rem"},
                    ),
                
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "padding": "1.5rem",
                        "textAlign": "center",
                    },
                ),

                id="upload",
                accept={"image/png": [".png"], "image/jpeg": [".jpeg", ".jpg"]},
                max_size=1024*1024*10, # 10 MB max limit for file uploads
                max_files=1,
                
                style={
                    "maxWidth": "24rem",
                    "height": "16rem",
                    "borderWidth": "2px",
                    "borderStyle": "dashed",
                    "borderColor": "#60a5fa",
                    "borderRadius": "0.75rem",
                    "cursor": "pointer",
                    "transitionProperty": "background-color",
                    "transitionDuration": "0.2s",
                    "transitionTimingFunction": "ease-in-out",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "boxShadow": "0 1px 2px rgba(0, 0, 0, 0.05)",
                },
            ),
            
            rx.input(
                placeholder="Enter a name for your note",
                id="name",
                max_length=30,
                style={
                    "align": "center",
                    "width": "200%",
                    "height": "12%",
                    "borderWidth": "0px",
                    "borderStyle": "dashed",
                    "borderColor": "#60a5fa",
                    "borderRadius": "0.75rem",
                    "padding": "1rem",
                    "marginTop": "1rem",
                    "fontSize": "1rem",
                    "color": "#4b5563",
                    "transitionProperty": "border-color, box-shadow",
                    "transitionDuration": "0.2s",
                    "transitionTimingFunction": "ease-in-out",
                    "outline": "none",
                    "boxShadow": "0 1px 2px rgba(0, 0, 0, 0.05)",
                },
            ),
            
            rx.button(
                "Upload",
                on_click= State.handleUpload(
                    rx.upload_files("upload") # type: ignore
                ),
            ),

            rx.text(rx.selected_files("upload")),

            rx.foreach(
                State.uploaded_files,
                lambda f: rx.image(
                    src=rx.get_upload_url(f),
                    style={"width": "300px", "height": "300px"},
                ),
            ),

            spacing="4",
            align="center",
        ),
        align_items="center",
        justify_content="center",
        height="100%",

    )

def landingPage() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to Note Taker!", font_size="2em", mb="2em", align="center"),
        rx.vstack(
            #rx.link("Login", href="/login", style={"textDecoration": "none"}),
            #rx.link("Sign Up", href="/signup", style={"textDecoration": "none"}),

            #TODO WARNING temporary
            rx.link("Upload", href="/upload", style={"textDecoration": "none"}, size="9"),

            align= "center",
            #spacing="1em"
        ),
        align_items="center",
        justify_content="center",
        height="100vh"
    )


app = rx.App()
app.add_page(landingPage, route="/")
app.add_page(uploadPage, route="/upload")

