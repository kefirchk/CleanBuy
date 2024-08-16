import hashlib


def generate_chat_id(user1_id: int, user2_id: int) -> str:
    ids = sorted([user1_id, user2_id])
    combined_ids = f"{ids[0]}_{ids[1]}"
    return hashlib.md5(combined_ids.encode()).hexdigest()
