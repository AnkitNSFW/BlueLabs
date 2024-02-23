import sys
sys.path.append('')

# JWT Utilities
import jwt
from credentials import jwt_secret_key
jwt_encode = lambda payload: jwt.encode(payload, jwt_secret_key, algorithm="HS256")
jwt_decode = lambda token: jwt.decode(token, jwt_secret_key, algorithms=["HS256"])


# OTP Utility
from random import randint
generate_otp = lambda: randint(111111,999999)


# SHA256 encoder - Double Hash
from hashlib import sha256
def to_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    sha256_hash = sha256(data).hexdigest()
    sha256_hash= sha256_hash.encode()
    sha256_hash = sha256(sha256_hash).hexdigest()
    return sha256_hash


# Translating datatime.now() time which is naive of timezone aware of timezone UTC
from pytz import utc
utc_translation = lambda time: utc.localize(time)


# Creating Unique UUID without '-'
from uuid import uuid4
create_uuid = lambda: str(uuid4()).replace('-', '')

import re
uuid4_pattern = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
check_uuid4 = lambda id: bool(uuid4_pattern.match(id))

# current date time
from django.utils import timezone
from datetime import datetime
current_DT = lambda: datetime.now(timezone.utc)