from __future__ import annotations
from dataclasses import dataclass
@dataclass
class Message:
    role:str; content:str; is_raw_tool_output:bool=False
class MemoryCompressor:
    def __init__(self,tool_output_head_chars=200): self.head_chars=tool_output_head_chars; self.last_stats={}
    def compress(self,messages):
        original=self._estimate_tokens(messages); compressed=[]
        for m in messages:
            if m.is_raw_tool_output and len(m.content)>self.head_chars:
                compressed.append(Message(m.role,m.content[:self.head_chars]+f"...[truncated {len(m.content)-self.head_chars} chars]",False))
            else: compressed.append(m)
        new=self._estimate_tokens(compressed); self.last_stats={"original_tokens":original,"compressed_tokens":new,"reduction_pct":round((1-new/original)*100,1) if original else 0.0}; return compressed
    @staticmethod
    def _estimate_tokens(messages): return max(1,sum(len(m.content) for m in messages)//2)
