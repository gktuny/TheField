from enum import Enum, auto
import time
import uuid

class ExistenceState(Enum):
    ACTIVE = auto()
    SILENT = auto()
    TERMINATING = auto()
    NON_EXISTENT = auto()

class RuntimeContext:
    def __init__(self):
        self.runtime_id = uuid.uuid4().hex
        self.state = ExistenceState.ACTIVE
        self.created_at = time.time()
        self.memory = {}
        self.identity = hash(self.runtime_id)

    def wipe_identity(self):
        self.memory.clear()
        self.identity = None