from enum import Enum

class clueStatus(Enum):
    CREATED = 1
    STARTED = 2
    PAUSED = 3
    DISCARDED = 4
    COMPLETED = 5