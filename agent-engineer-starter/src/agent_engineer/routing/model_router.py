from __future__ import annotations
from dataclasses import dataclass
from ..config import CONFIG
@dataclass
class RouteDecision:
    model_tier:str; estimated_cost:float; estimated_latency_ms:int; reason:str
class ModelRouter:
    def __init__(self,price_per_1k=None):
        self.price_per_1k=price_per_1k or CONFIG.price_per_1k
        self.latency_map={"light":300,"standard":1200,"reasoning":3500}; self.stats=[]
    def route(self,token_count,needs_reasoning,tool_depth):
        if needs_reasoning or tool_depth>=CONFIG.reasoning_tool_depth: tier,reason="reasoning","复杂规划或长工具链"
        elif token_count>CONFIG.standard_token_threshold or tool_depth==2: tier,reason="standard","中等复杂度"
        else: tier,reason="light","简单任务"
        cost=self.price_per_1k[tier]*token_count/1000; self.stats.append({"tier":tier,"tokens":token_count,"cost":cost})
        return RouteDecision(tier,round(cost,6),self.latency_map[tier],reason)
    def cost_summary(self):
        total=sum(x["cost"] for x in self.stats); baseline=sum(self.price_per_1k["reasoning"]*x["tokens"]/1000 for x in self.stats)
        return {"total_cost":round(total,6),"reasoning_only_baseline":round(baseline,6),"saving_pct":round((1-total/baseline)*100,1) if baseline else 0.0,"calls":len(self.stats),"tier_distribution":self._tier_distribution()}
    def _tier_distribution(self):
        result={}
        for item in self.stats: result[item["tier"]]=result.get(item["tier"],0)+1
        return result
