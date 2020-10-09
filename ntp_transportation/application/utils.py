from enum import Enum


class RoleEnum(Enum):
    ADMIN = "Admin"
    REGISTERED_USER = "Registered User"
    NONE = "None"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]