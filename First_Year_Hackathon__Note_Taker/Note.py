import math
import sqlite3
from typing import Literal, List, Optional

class NoteDAO:
    def __init__(self, db_path: str = "NotesDB"):
        self.db_path = db_path

    def _getConnection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn

    """_DB suffix in the function name siginifies DAO function"""

    def update_academic_level(self, note_id: int, academic_level: Literal["GCSE", "A Level", "Degree"]) -> bool:
        """Update academic level for a note"""
        try:
            # Convert to database format while keeping your original values
            db_academic_level = self._convert_academic_level_to_db(academic_level)
            
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET academic_level = ? WHERE id = ?", 
                (db_academic_level, note_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update_academic_level: {e}")
            return False
        finally:
            conn.close()

    def get_academic_level(self, note_id: int) -> Optional[str]:
        """Get academic level for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT academic_level FROM notes WHERE id = ?", 
                (note_id,)
            )
            result = cursor.fetchone()
            if result and result[0]:
                # Convert back from database format to your format
                return self._convert_academic_level_from_db(result[0])
            return None
        except sqlite3.Error as e:
            print(f"Database error in get_academic_level: {e}")
            return None
        finally:
            conn.close()

    def _convert_academic_level_to_db(self, academic_level: str) -> str:
        """Convert your academic level format to database format"""
        if academic_level == "A Level":
            return "A-Level"
        elif academic_level == "Degree":
            return "University"
        else:
            return academic_level  # "GCSE" stays the same

    def _convert_academic_level_from_db(self, db_academic_level: str) -> str:
        """Convert database academic level format to your format"""
        if db_academic_level == "A-Level":
            return "A Level"
        elif db_academic_level == "University":
            return "Degree"
        else:
            return db_academic_level  # "GCSE" stays the same

    # ========== VOTE METHODS ==========

    def update_upvotes(self, note_id: int, upvotes: int) -> bool:
        """Update upvotes count for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET upvote = ? WHERE id = ?", 
                (upvotes, note_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update_upvotes: {e}")
            return False
        finally:
            conn.close()

    def get_upvotes(self, note_id: int) -> Optional[int]:
        """Get upvotes count for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT upvote FROM notes WHERE id = ?", 
                (note_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_upvotes: {e}")
            return None
        finally:
            conn.close()

    def update_downvotes(self, note_id: int, downvotes: int) -> bool:
        """Update downvotes count for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET downvote = ? WHERE id = ?", 
                (downvotes, note_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update_downvotes: {e}")
            return False
        finally:
            conn.close()

    def get_downvotes(self, note_id: int) -> Optional[int]:
        """Get downvotes count for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT downvote FROM notes WHERE id = ?", 
                (note_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_downvotes: {e}")
            return None
        finally:
            conn.close()

    def increment_upvotes(self, note_id: int) -> bool:
        """Increment upvotes by 1"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET upvote = upvote + 1 WHERE id = ?", 
                (note_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in increment_upvotes: {e}")
            return False
        finally:
            conn.close()

    def increment_downvotes(self, note_id: int) -> bool:
        """Increment downvotes by 1"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET downvote = downvote + 1 WHERE id = ?", 
                (note_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in increment_downvotes: {e}")
            return False
        finally:
            conn.close()

    def decrement_upvotes(self, note_id: int) -> bool:
        """Decrement upvotes by 1"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET upvote = upvote - 1 WHERE id = ?", 
                (note_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in decrement_upvotes: {e}")
            return False
        finally:
            conn.close()

    def decrement_downvotes(self, note_id: int) -> bool:
        """Decrement downvotes by 1"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET downvote = downvote - 1 WHERE id = ?", 
                (note_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in decrement_downvotes: {e}")
            return False
        finally:
            conn.close()

    def get_vote_ratio(self, note_id: int) -> Optional[float]:
        """Get vote ratio for a note"""
        try:
            upvotes = self.get_upvotes(note_id)
            downvotes = self.get_downvotes(note_id)
            
            if upvotes is None or downvotes is None:
                return None
                
            total_votes = upvotes + downvotes
            if total_votes == 0:
                return 0.0
                
            return math.floor(upvotes / total_votes)
        except Exception as e:
            print(f"Error in get_vote_ratio: {e}")
            return None

    # ========== VISIBILITY METHODS ==========

    def update_visibility(self, note_id: int, visibility: Literal["public", "private"]) -> bool:
        """Update note visibility"""
        try:
            # Convert to database format
            db_visibility = visibility.capitalize()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET visibility = ? WHERE id = ?", 
                (db_visibility, note_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update_visibility: {e}")
            return False
        finally:
            conn.close()

    def get_visibility(self, note_id: int) -> Optional[str]:
        """Get note visibility"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT visibility FROM notes WHERE id = ?", 
                (note_id,)
            )
            result = cursor.fetchone()
            if result and result[0]:
                # Convert back from database format to your format
                return result[0].lower()
            return None
        except sqlite3.Error as e:
            print(f"Database error in get_visibility: {e}")
            return None
        finally:
            conn.close()

    # ========== TAG METHODS ==========

    def update_tags(self, note_id: int, tags: List[str]) -> bool:
        """Update tags for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            tags_string = ",".join(tags) if tags else None
            cursor.execute(
                "UPDATE notes SET tags = ? WHERE id = ?", 
                (tags_string, note_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update_tags: {e}")
            return False
        finally:
            conn.close()

    def get_tags(self, note_id: int) -> List[str]:
        """Get tags for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tags FROM notes WHERE id = ?", 
                (note_id,)
            )
            result = cursor.fetchone()
            if result and result[0]:
                return [tag.strip() for tag in result[0].split(',')]
            return []
        except sqlite3.Error as e:
            print(f"Database error in get_tags: {e}")
            return []
        finally:
            conn.close()

    def add_tag(self, note_id: int, tag: str) -> bool:
        """Add a single tag to a note"""
        try:
            current_tags = self.get_tags(note_id)
            if tag in current_tags:
                return False  # Tag already exists
            
            current_tags.append(tag)
            return self.update_tags(note_id, current_tags)
        except sqlite3.Error as e:
            print(f"Database error in add_tag: {e}")
            return False

    def remove_tag(self, note_id: int, tag: str) -> bool:
        """Remove a single tag from a note"""
        try:
            current_tags = self.get_tags(note_id)
            if tag not in current_tags:
                return False  # Tag doesn't exist
            
            current_tags.remove(tag)
            return self.update_tags(note_id, current_tags)
        except sqlite3.Error as e:
            print(f"Database error in remove_tag: {e}")
            return False

    def has_tag(self, note_id: int, tag: str) -> bool:
        """Check if note has a specific tag"""
        tags = self.get_tags(note_id)
        return tag in tags

    # ========== USER AND IMAGE METHODS ==========

    def get_user_id(self, note_id: int) -> Optional[int]:
        """Get user ID for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT userid FROM notes WHERE id = ?", 
                (note_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_user_id: {e}")
            return None
        finally:
            conn.close()

    def get_image_id(self, note_id: int) -> Optional[int]:
        """Get image ID for a note"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT imageid FROM notes WHERE id = ?", 
                (note_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_image_id: {e}")
            return None
        finally:
            conn.close()

    # ========== UTILITY METHODS ==========

    def note_exists(self, note_id: int) -> bool:
        """Check if a note exists"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
            result = cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"Database error in note_exists: {e}")
            return False
        finally:
            conn.close()
    
    
    def setAcademicLevel_DB(self, user_id: int, academic_level: str) -> bool:
        try:
            # Validate the academic level matches your database CHECK constraint
            if academic_level not in ['GCSE', 'A Level', 'Degree']:
                print(f"Invalid academic level: {academic_level}")
                return False

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # UPDATE the academic_level for the specific user
            cursor.execute(
                'UPDATE users SET academic_level = ? WHERE id = ?', 
                (academic_level, user_id)
            )
            conn.commit()

            # Return True if the update was successful (user exists and was updated)
            return cursor.rowcount > 0

        except sqlite3.Error as e:
            print(f'Database Error: {e}')
            return False
        finally:
            conn.close()

    



class Note(NoteDAO):
    # Initialize a new note object, given paramaters
    def __init__(self, id: int, userid: int, imageid: int, tags: List[str], visbility: Literal["public", "private"], academicLevel: Literal["GCSE", "A Level", "Degree"]):
        assert id > 0, "Note ID must be greater than 0"
        assert userid > 0, "User ID must be greater than 0"
        assert imageid > 0, "Image ID must be greater than 0"
        assert academicLevel == "GCSE" or academicLevel == "A Level" or academicLevel == "Degree", "Academic Level must be GCSE, A Level or Degree"
       
        super().__init__() # Call the initalisation of NoteDAO

        self.id = id
        self.userid = userid
        self.imageid = imageid
        self.tags = tags
        self.visibility = visbility
        self.upvotes = 0
        self.downvotes = 0
        self.academicLevel = academicLevel
    
    # Set the academic level of the note
    def setAcademicLevel(self, academicLevel: Literal["GCSE", "A Level", "Degree"]):
        assert academicLevel == "GCSE" or academicLevel == "A Level" or academicLevel == "Degree", "Academic Level must be GCSE, A Level or Degree"
        self.academicLevel = academicLevel
        return
    
    # Get the academic level of the note
    def getAcademicLevel(self) -> str:
        return self.academicLevel

    # Set the upvotes of the note
    def setUpvotes(self, upvotes: int):
        self.upvotes = upvotes
        return
    
    # Get the upvotes of the note
    def getUpvotes(self) -> int:
        return self.upvotes

    # Set the downvotes of the note
    def setDownvotes(self, downvotes: int):
        self.downvotes = downvotes
        return

    # Get the downvotes of the note
    def getDownvotes(self) -> int:
        return self.downvotes

    # Increment the upvotes of the note
    def incrementUpvotes(self):
        self.upvotes += 1
        return

    # Increment the downvotes of the note
    def incrementDownvotes(self):
        self.downvotes += 1
        return
    
    # Decrement the upvotes of the note
    def decrementUpvotes(self):
        self.upvotes -= 1
        return
    
    # Decrement the downvotes of the note
    def decrementDownvotes(self):
        self.downvotes -= 1
        return

    # Get the vote ratio of the note
    def getVoteRatio(self) -> int:
        return math.floor(self.upvotes / (self.upvotes + self.downvotes))
   
    # Set the visibility of the note
    # visbility can be "public" or "private"
    def setVisibility(self, visbility: Literal["public", "private"]):
        assert visbility == "public" or visbility == "private", "Visibility must be public or private"
        self.visibility = visbility
        return
    
    # Get the visibility of the note
    def getVisibility(self) -> str:
        return self.visibility
    
    def addTag(self, tag: str):
        assert tag not in self.tags, "Tag already exists"
        self.tags.append(tag)
        return
    
    def removeTag(self, tag: str):
        assert tag in self.tags, "Tag does not exist"
        self.tags.remove(tag)
        return 
    
    def hasTag(self, tag: str) -> bool:
        return tag in self.tags
    
    def getTags(self) -> list[str]:
        return self.tags
    
    def getUserId(self) -> int:
        return self.userid
    
    def getImageId(self) -> int:    
        return self.imageid
