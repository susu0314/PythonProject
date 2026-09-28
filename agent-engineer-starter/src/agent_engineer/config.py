from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
@dataclass
class AgentConfig:
    env: str = os.getenv("AGENT_ENV", "dev")
    log_level: str = os.getenv("AGENT_LOG_LEVEL", "INFO")
    audit_log_path: Path = Path(os.getenv("AGENT_AUDIT_LOG", "./audit.log"))
    max_retry: int = int(os.getenv("AGENT_MAX_RETRY", "2"))
    pii_redaction: bool = os.getenv("AGENT_PII_REDACTION", "true").lower() == "true"
    price_per_1k: dict[str,float] = field(default_factory=lambda: {"light":0.00015,"standard":0.003,"reasoning":0.015})
    standard_token_threshold: int = 2000
    reasoning_tool_depth: int = 3
CONFIG = AgentConfig()
