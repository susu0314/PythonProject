from __future__ import annotations
import time,json
from dataclasses import dataclass,field
from .config import CONFIG
from .contracts.structured_contract import TicketResult,validate_ticket_output
from .fallback.fallback_orchestrator import FallbackLevel,FallbackOrchestrator
from .memory.memory_compressor import MemoryCompressor,Message
from .observability.audit_logger import AuditEvent,AuditLogger
from .routing.model_router import ModelRouter
from .safety.safety_guardrail import SafetyGuard
@dataclass
class PipelineResult:
    success:bool; level:FallbackLevel; tier:str; cost_usd:float; latency_ms:int
    output:TicketResult|None=None; raw_output:str|None=None; redacted_output:str|None=None; error:str|None=None; audit_events:int=0; memory_stats:dict=field(default_factory=dict)
class AgentPipeline:
    def __init__(self,router=None,guard=None,fallback=None,compressor=None,audit=None,model_callable=None):
        self.router=router or ModelRouter(); self.guard=guard or SafetyGuard(); self.fallback=fallback or FallbackOrchestrator(); self.compressor=compressor or MemoryCompressor(); self.audit=audit or AuditLogger(CONFIG.audit_log_path); self.model_callable=model_callable or self._stub_model_call
    def run(self,prompt,tool_name,token_count=1200,needs_reasoning=False,tool_depth=1,user_id="anonymous",trace_id=None):
        t0=time.time(); trace_id=trace_id or f"tr-{int(t0*1000)}"; d=self.router.route(token_count,needs_reasoning,tool_depth)
        self.audit.log(AuditEvent(t0,"INFO","route_decision",user_id=user_id,trace_id=trace_id,payload={"tier":d.model_tier,"reason":d.reason}))
        allowed,reason=self.guard.check_tool(tool_name); self.audit.log(AuditEvent(time.time(),"INFO" if allowed else "WARN","guardrail_check",tool=tool_name,user_id=user_id,trace_id=trace_id,payload={"allowed":allowed,"reason":reason}))
        if not allowed:
            level=self.fallback.decide("dangerous_tool",0); self.audit.log(AuditEvent(time.time(),"WARN","fallback",user_id=user_id,trace_id=trace_id,payload={"level":level.value,"reason":reason}))
            return PipelineResult(False,level,d.model_tier,d.estimated_cost,int((time.time()-t0)*1000),error=reason,audit_events=len(self.audit.buffer))
        retry=0; feedback=None
        while True:
            raw=self.model_callable(prompt,d.model_tier,token_count); ok,feedback,parsed=validate_ticket_output(raw)
            self.audit.log(AuditEvent(time.time(),"INFO" if ok else "WARN","schema_validation",user_id=user_id,trace_id=trace_id,payload={"ok":ok,"retry":retry}))
            if ok and parsed is not None: break
            level=self.fallback.decide("schema_invalid",retry)
            if level!=FallbackLevel.RETRY: return PipelineResult(False,level,d.model_tier,d.estimated_cost,int((time.time()-t0)*1000),raw_output=raw,error=feedback,audit_events=len(self.audit.buffer))
            retry+=1; prompt=f"{prompt}\n\n[上一轮校验失败反馈]\n{feedback}"
        self.compressor.compress([Message("user",prompt),Message("tool",raw,True)])
        redacted=self.guard.redact_outbound(raw) if CONFIG.pii_redaction else raw
        self.audit.log(AuditEvent(time.time(),"INFO","completed",user_id=user_id,trace_id=trace_id,payload={"tier":d.model_tier,"cost_usd":d.estimated_cost,"retry":retry}))
        return PipelineResult(True,FallbackLevel.RETRY if retry else FallbackLevel.SAFE_REPLY,d.model_tier,d.estimated_cost,int((time.time()-t0)*1000),output=parsed,raw_output=raw,redacted_output=redacted,audit_events=len(self.audit.buffer),memory_stats=self.compressor.last_stats)
    @staticmethod
    def _stub_model_call(prompt,tier,token_count):
        p=prompt.lower(); category="billing" if ("billing" in p or "退款" in prompt or "账单" in prompt) else ("technical" if ("error" in p or "timeout" in p or "故障" in prompt) else "other")
        return json.dumps({"category":category,"confidence":0.92,"reason":f"基于离线 Stub 与 {tier} 档路由演示","priority":"medium"},ensure_ascii=False)
