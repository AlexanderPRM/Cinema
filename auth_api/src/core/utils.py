import uuid


def is_uuid_valid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
