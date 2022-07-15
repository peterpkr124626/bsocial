from passlib.context import CryptContext


def hash_password(password):
    hashed_password = password_context.hash(password)
    return hashed_password


def verify(attempted_password, hashed_password):
    return password_context.verify(attempted_password, hashed_password)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
