import datetime

# Date time format
DATE_FORMAT = "%d/%m/%Y"
DB_FORMAT = "%d-%m-%Y"

class User:
    def __init__(self, id: int, name: str, email: str, password: str, credits: int, dob: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.credits = credits
        self.isPremium = False # All accounts begin as free accounts
        # Keep images as .png for SQL compatibility
        self.pfp_url = "https://github.com/thekuddlekoala/First-Year-Hackathon--Note-Taker/blob/65098634cefbed156726c3657a1a14e94680741c/assets/defaultuser.png?raw=true"  
        self.dob = dob.strftime(datetime.strptime(dob, DB_FORMAT))

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
            self.password = new_password
        else:
            print('Temp error: Current user ID does not exist')
        
    
def has_special_chars(p):
            for letter in p:
                if not (letter.isalpha() or letter.isdigit() or letter == " "):
                    return True
            return False
        
        
        #All the relevant validation for fields
        
        # def validate_email_syntax(email):
        #     pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" #Function to validate whether the email is of the correct form.
        #     return re.match(pattern, email) is not None
            
        # if validate_email_syntax(email) == False:
        #     flash("Email not valid", category="error")
        # #Checks if firstName/lastName has only letters and is more than 2 characters long
        # elif len(firstName) < 2:
        #     flash("Length of first name must be more than 2 characters", category="error")
        # elif len(lastName) < 2:
        #     flash("Length of last name must be more than 2 characters", category="error")
        # elif any(char.isdigit() for char in firstName) == True or has_special_chars(firstName) == True:
        #     flash("First Names must not have special characters/numbers", category="error")
        # elif any(char.isdigit() for char in lastName) == True or has_special_chars(lastName) == True:
        #     flash("Last Names must not have special characters/numbers", category="error")
        # #Checks if password and confirm password match. 
        # #Checks if it contains at least 1 special character, number, lower/uppercase character and is at least 8 characters.
        # elif password1 != password2:   
        #     flash("Passwords do not match", category="error")
        # elif len(password1) < 8:
        #     flash("Password must be greater than 8 characters in length", category="error")
        # elif any(char.isdigit() for char in password1) == False:
        #     flash("Password does not contain a number", category="error")
        # elif any(char.isupper() for char in password1) == False:
        #     flash("Password does not contain an uppercase character", category="error")
        # elif any(char.islower() for char in password1) == False:
        #     flash("Password does not contain an lowercase character", category="error")
        # elif has_special_chars(password1) == False:
        #     flash("Passwords do not contain special characters", category="error")
        # else:
        #     print("Hello")
        #     if user_type == "tutor":
        #         new_tutor = Tutor(f_name=firstName, s_name=lastName, email=email, user_password=generate_password_hash(password1, method="pbkdf2:sha256"))
        #         db.session.add(new_tutor)
        #         db.session.commit()
        #         print("Added")
        #     elif user_type == "student":
        #         new_student = Student(f_name=firstName, s_name=lastName, email=email, user_password=generate_password_hash(password1, method="pbkdf2:sha256"))
        #         db.session.add(new_student)
        #         db.session.commit()
        #         print("Added")