import math 

class Note:
    def __init__(self, id: int, userid: int, imageid: int, tags: list[str], visbility: str, academicLevel: str):
        assert id > 0, "Note ID must be greater than 0"
        assert userid > 0, "User ID must be greater than 0"
        assert imageid > 0, "Image ID must be greater than 0"
        assert academicLevel == "GCSE" or academicLevel == "A Level" or academicLevel == "Degree" 
       
        self.id = id
        self.userid = userid
        self.imageid = imageid
        self.tags = tags
        self.visibility = visbility
        self.upvotes = 0
        self.downvotes = 0
        self.academicLevel = academicLevel
    
    def setAcademicLevel(self, academicLevel: str):
        assert academicLevel == "GCSE" or academicLevel == "A Level" or academicLevel == "Degree"
        self.academicLevel = academicLevel
        return
    
    def getAcademicLevel(self) -> str:
        return self.academicLevel

    def setUpvotes(self, upvotes: int):
        self.upvotes = upvotes
        return

    def getUpvotes(self) -> int:
        return self.upvotes

    def setDownvotes(self, downvotes: int):
        self.downvotes = downvotes
        return

    def getDownvotes(self) -> int:
        return self.downvotes

    def incrementUpvotes(self):
        self.upvotes += 1
        return

    def incrementDownvotes(self):
        self.downvotes += 1
        return
    
    def getVoteRatio(self) -> int:
        return math.floor(self.upvotes / (self.upvotes + self.downvotes))

    def setVisibility(self, visbility: str):
        assert visbility == "public" or visbility == "private", "Visibility must be public or private"
        self.visibility = visbility
        return
    
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