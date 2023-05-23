def generate_token(username: str, id: int = 0) -> str:
    return f"{id}_{username}_{id}"
