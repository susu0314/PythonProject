from rich.console import Console
from rich.table import Table
from agent_engineer.pipeline import AgentPipeline
def main():
    p=AgentPipeline(); trace="f561a01f69e9e2a3"; steps=[("query_endpoint_errors",1500),("query_trace",3200),("query_metrics",2800)]
    t=Table(title="运维排障 Agent 链路")
    for c in ["步骤","工具","档位","成本($)","状态"]: t.add_column(c)
    for i,(tool,tokens) in enumerate(steps,1):
        r=p.run(f"排障步骤 {i}",tool,tokens,needs_reasoning=tokens>3000,tool_depth=i,trace_id=trace)
        t.add_row(str(i),tool,r.tier,f"{r.cost_usd:.6f}","OK" if r.success else "BLOCKED")
    Console().print(t); Console().print("TraceID:",trace); Console().print(p.router.cost_summary())
if __name__=="__main__": main()
