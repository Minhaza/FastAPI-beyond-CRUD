from passlib.context import CryptContext

pw_context = CryptContext(schemes=['bcrypt'])

def generate_password_hash(password: str) -> str:
    hash = pw_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return pw_context.verify(password, hash)
    