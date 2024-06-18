from passlib.context import CryptContext

# Initialize CryptContext with bcrypt hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    # Generate a hashed password using bcrypt
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    # Verify if the plain password matches the hashed password
    return pwd_context.verify(plain_password, hashed_password)
