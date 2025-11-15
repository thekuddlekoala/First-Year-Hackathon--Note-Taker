import hashlib 

# Hash a given string using the sha256 encryption algorithm
def encryptSHA256(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()