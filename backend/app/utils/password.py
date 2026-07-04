import random
import string
import bcrypt

def hash_password(password: str) -> str:
    # bcrypt requires passwords to be bytes, and has a 72-byte limit.
    # We encode to utf-8 and truncate to 72 bytes to avoid the ValueError.
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode('utf-8')[:72]
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def generate_temp_password(length: int = 8) -> str:
    chars = string.ascii_letters + string.digits
    while True:
        pwd = ''.join(random.choice(chars) for _ in range(length))
        if (any(c.isupper() for c in pwd) and 
            any(c.islower() for c in pwd) and 
            any(c.isdigit() for c in pwd)):
            return pwd