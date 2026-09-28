from enum import Enum
from ..config import CONFIG
class FallbackLevel(Enum):
    RETRY="L1_retry"; SAFE_REPLY="L2_safe_reply"; HUMAN="L3_human"
class FallbackOrchestrator:
    def __init__(self,max_retry=None): self.max_retry=max_retry if max_retry is not None else CONFIG.max_retry
    def decide(self,failure_type,retry_count):
        if failure_type=="dangerous_tool": return FallbackLevel.HUMAN
        if failure_type=="schema_invalid": return FallbackLevel.RETRY if retry_count<self.max_retry else FallbackLevel.SAFE_REPLY
        return FallbackLevel.HUMAN
