import bcrypt

# lazy

def encrypt(password):
    encrypted_password = (f"salty{password[::-1]}moresalty").encode("utf-8")
    hashedPassword = bcrypt.hashpw(encrypted_password, bcrypt.gensalt())
    return hashedPassword

def verify_password(password, encryptedPassword):
    password = f"salty{password[::-1]}moresalty".encode("utf-8")

    return bcrypt.checkpw(password, encryptedPassword)
