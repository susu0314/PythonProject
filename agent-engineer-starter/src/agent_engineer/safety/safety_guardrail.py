from __future__ import annotations
import re
from dataclasses import dataclass,field
@dataclass
class GuardrailPolicy:
    allow:list[str]=field(default_factory=lambda:["get_order_status","search_faq","query_metrics","query_trace","query_endpoint_errors"])
    deny:list[str]=field(default_factory=lambda:["issue_refund","delete_volume","mass_email","exec_shell","drop_database"])
    rate_limits:dict[str,int]=field(default_factory=lambda:{"get_order_status":5,"query_metrics":3,"query_trace":5})
class SafetyGuard:
    _PII_PATTERNS=[(r"sk-ant-[A-Za-z0-9_-]{20,}","[REDACTED_API_KEY]"),(r"sk-[A-Za-z0-9]{20,}","[REDACTED_API_KEY]"),(r"\b\d{3}-\d{2}-\d{4}\b","[REDACTED_SSN]"),(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b","[REDACTED_EMAIL]"),(r"\b(?:\d[ -]?){13,16}\b","[REDACTED_CARD]"),(r"\b1[3-9]\d{9}\b","[REDACTED_PHONE]")]
    def __init__(self,policy=None): self.policy=policy or GuardrailPolicy(); self.call_counts={}; self.decisions=[]
    def check_tool(self,tool_name):
        if tool_name in self.policy.deny:
            msg=f"工具 '{tool_name}' 在 deny 列表中，禁止执行"; self._record(tool_name,False,"deny_list"); return False,msg
        if tool_name not in self.policy.allow:
            msg=f"工具 '{tool_name}' 未在 allow 列表中，默认拒绝"; self._record(tool_name,False,"not_in_allow"); return False,msg
        limit=self.policy.rate_limits.get(tool_name)
        if limit is not None:
            used=self.call_counts.get(tool_name,0)
            if used>=limit:
                msg=f"工具 '{tool_name}' 已达速率限制 ({limit} 次/会话)"; self._record(tool_name,False,"rate_limit"); return False,msg
            self.call_counts[tool_name]=used+1
        self._record(tool_name,True,"ok"); return True,""
    def redact_outbound(self,text):
        for pattern,replacement in self._PII_PATTERNS: text=re.sub(pattern,replacement,text)
        return text
    def _record(self,tool,allowed,reason): self.decisions.append({"tool":tool,"allowed":allowed,"reason":reason})
