from datetime import datetime
from Common import encryptSHA256
import sqlite3

# Date time format
DATE_FORMAT = "%d/%m/%Y"
DB_FORMAT = "%d-%m-%Y"

class UserDAO:
    def __init__(self, db_path: str = "NotesDB"):
        self.db_path = db_path
    
    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn

    def user_exists(self, user_id: int) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
        
            cursor = conn.cursor()
            cursor.execute(f'SELECT id FROM users WHERE id = ?', (user_id))
            res = cursor.fetchone() # Attempt to locate a row where the user's ID exists

            return res is not None # Return true if the user's ID exists
        
        except sqlite3.Error as e:
            print(f'Database Error: {e}')
            return False

        finally:
            conn.close()

class User(UserDAO):
    def __init__(self, id: int, name: str, email: str, password: str, credits: int, dob: str):
        super().__init__() # Call the init of UserDAO

        self.id = id
        self.name = name
        self.password = password
        self.credits = credits
        self.isPremium = False # All accounts begin as free accounts
        # Keep images as .png for SQL compatibility
        self.dob = datetime.strptime(dob, DB_FORMAT).strftime(DATE_FORMAT)
        self.pfp_url = "https://github.com/thekuddlekoala/First-Year-Hackathon--Note-Taker/blob/65098634cefbed156726c3657a1a14e94680741c/assets/defaultuser.png?raw=true"  
        self.email = email

    def changeCredits(self, new_credits: int):
        if self.id: # Proper exception handling to be added once databse is fully implemeneted
            self.credits = new_credits if new_credits >= 0 else 0
        else:
            print('Temp error: Current user ID does not exist')

    def changePremium(self, state: bool):
        if self.id: # Proper exception handling to be added once databse is fully implemeneted
            self.isPremium = state
        else:
            print('Temp error: Current user ID does not exist')

    def changeProfileImage(self, img_url: str):
        if self.id: # Proper exception handling to be added once databse is fully implemeneted
            self.pfp_url = img_url
        else:
            print('Temp error: Current user ID does not exist')

    def changePassword(self, new_password: str):
        if self.id: # Proper exception handling to be added once databse is fully implemeneted
            self.password = encryptSHA256(new_password)
        else:
            print('Temp error: Current user ID does not exist')
