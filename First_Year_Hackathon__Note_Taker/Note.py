import math
import sqlite3
from typing import Literal, List

class NoteDAO:
    def __init__(self, db_path: str = "NotesDB"):
        self.db_path = db_path

    def _getConnection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn

    def get_note_tags_from_db(self, note_id: int) -> List[str]:
        try:
            conn = self._getConnection(self)
            cursor = conn.cursor()

            cursor.execute()
            
            cursor.execute("SELECT tags FROM notes WHERE id = ?", (note_id,))
            result = cursor.fetchone()

            if result and result[0]:
                tags = [tag.strip() for tag in result[0].split(',')]
                return tags
            return []
    
        except sqlite3.Error as e:
            print(f'Database error: {e}')
            return []
    
        finally:
            conn.close()
    
    def refresh_tags_from_db(self) -> bool:
        db_tags = self.get_note_tags_from_db(self.id)  # Calls inherited NoteDAO method

        if db_tags is not None:
            self.tags = db_tags
            return True
        
        return False


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
