import hmac
import hashlib
import os
import time

secret = str(os.getenv("HASHING_SECRET"))
validity = int(os.getenv("HASH_VALIDITY", 30))


def generate_hash(user_id: int) -> str:
    """
    generate hash in the following format:
    user_id : number of seconds elapsed since the Unix epoch rounded off by specified validity
    """

    # Number of seconds elapased since the Unix epoch rounded off with the validity
    seconds_since_unix_epoch = int(round(time.time()) / validity)

    message = f"{user_id}:{seconds_since_unix_epoch}"

    hashed = hmac.new(
        bytes(secret, "utf8"), bytes(message, "utf8"), hashlib.sha256
    ).hexdigest()

    return f"{message}::{hashed}"


def verify_hash(message: str) -> bool:
    """
    verify QR integrity and expiration

    expected format:
        user id : number of seconds elapsed since the Unix epoch rounded off by specified validity :: the same thing, hashed

    """

    original_message, hashed_message = message.split("::")
    user_id, time_of_generation = original_message.split(":")

    server_time = int(round(time.time()) / validity)

    if int(time_of_generation) < server_time:
        return False
    else:
        return (
            hmac.new(
                bytes(secret, "utf8"),
                bytes(f"{user_id}:{time_of_generation}", "utf8"),
                hashlib.sha256,
            ).hexdigest()
            == hashed_message
        )


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
