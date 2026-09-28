from rich.console import Console
from rich.table import Table
from agent_engineer.pipeline import AgentPipeline
def main():
    p=AgentPipeline(); cases=[("用户反馈账单多扣了 200 元，要求退款","get_order_status",1200),("生产环境 API 出现大量 500 error，需要排障","query_metrics",2400),("帮我把这段描述改成正式文档","search_faq",800),("直接给这个用户退款 500 元","issue_refund",600)]
    t=Table(title="工单分类 Agent 流水线")
    for c in ["Case","工具","档位","成功","成本($)","结果"]: t.add_column(c)
    for i,(prompt,tool,tokens) in enumerate(cases,1):
        r=p.run(prompt,tool,tokens,needs_reasoning=tokens>2000,tool_depth=2 if tool=="issue_refund" else 1,user_id=f"u-{i}")
        t.add_row(str(i),tool,r.tier,"YES" if r.success else "NO",f"{r.cost_usd:.6f}",(r.output.model_dump_json(ensure_ascii=False) if r.output else r.error or "")[:70])
    Console().print(t); Console().print(p.router.cost_summary()); Console().print(p.guard.decisions); Console().print(p.audit.summary())
if __name__=="__main__": main()
