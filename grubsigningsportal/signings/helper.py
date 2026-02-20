import hmac
import hashlib
import os
import time

secret = str(os.getenv("HASHING_SECRET"))
validity = int(os.getenv("HASH_VALIDITY", 30))


def generate_hash(uid: int) -> str:
    """
    generate hash in a predefined format
    """

    unix = int(round(time.time()) / validity)
    message = f"{uid}:{unix}"
    hashed = hmac.new(
        bytes(secret, "utf8"), bytes(message, "utf8"), hashlib.sha256
    ).hexdigest()
    return f"{message}::{hashed}"


def verify_hash(data: str) -> bool:
    """
    verify integrity and expiration
    """
    uid = data.split(":")[0]
    unix = data.split(":")[1].split("::")[0]
    hashed = data.split("::")[1]

    if int(unix) < int(round(time.time()) / validity):
        return False
    elif (
        hmac.new(
            bytes(secret, "utf8"), bytes(f"{uid}:{unix}", "utf8"), hashlib.sha256
        ).hexdigest()
        == hashed
    ):
        return True
    else:
        return False


# if __name__ == "__main__":
#     """
#     testing expiry and generation
#     """
#     print(generate_hash(5760))
#     while True:
#         a = generate_hash(5760)
#         start = round(time.time())
#         while True:
#             time.sleep(1)
#             if not verify_hash(a):
#                 end = round(time.time())
#                 print(f"Hash changed after {end-start} seconds")
#                 break
