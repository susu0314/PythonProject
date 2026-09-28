from __future__ import annotations
import json,time
from dataclasses import asdict,dataclass,field
from pathlib import Path
from typing import Any
@dataclass
class AuditEvent:
    ts:float; level:str; event_type:str; tool:str|None=None; user_id:str|None=None; trace_id:str|None=None; payload:dict[str,Any]=field(default_factory=dict)
class AuditLogger:
    def __init__(self,path="./audit.log"): self.path=Path(path); self.buffer=[]
    def log(self,event):
        if isinstance(event,dict): event=AuditEvent(event.get("ts",time.time()),event.get("level","INFO"),event.get("event_type","unknown"),event.get("tool"),event.get("user_id"),event.get("trace_id"),event.get("payload",{}))
        self.buffer.append(event); self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(asdict(event),ensure_ascii=False)+"\n")
    def summary(self):
        counts={}
        for e in self.buffer: counts[e.event_type]=counts.get(e.event_type,0)+1
        return {"total":len(self.buffer),"by_type":counts}
