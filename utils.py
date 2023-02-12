SAFE_LIMIT = 1500
WARN_LIMIT = 2000


def get_status(x) -> str:
    if x <= SAFE_LIMIT:
        return "SAFE"
    if x <= WARN_LIMIT:
        return "WARNING"
    return "DANGER"
