from datetime import datetime, timedelta
from decouple import config
from jose import jwt
import uuid

JWT_SECRET = config("JWT_SECRET")

def issue_access_token(sub: uuid.UUID):
    payload = {
        "sub": str(sub),
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, JWT_SECRET)
    return token