import hashlib 
import re

# Hash a given string using the sha256 encryption algorithm
def encryptSHA256(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()
    
# Subroutine for password validation
def enterPassword(pw_input: str) -> str:
    PASSWORD_PATTERN = r'^(?=.*[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?])(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]{8,}$'

    while not re.match(PASSWORD_PATTERN, pw_input):
        pass
        # Add exception handling for front end where applicable
    
    return encryptSHA256(pw_input)

# Subroutine for email validation
def enterEmail(email_input: str) -> str:
    EMAIL_PATTERN = r'^(?![.-])[a-zA-Z0-9._%+-]+(?<![.-])@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$'

    while not re.match(EMAIL_PATTERN, email_input):
        pass
        # Add exception handling for front end where applicable
    
    return email_input

# Date of birth validation
def enterDOB() -> str:
    year_int = int(input)
    
    days_in_month = {
        1: 31, 2: 29 if (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0) else 28,
        3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }