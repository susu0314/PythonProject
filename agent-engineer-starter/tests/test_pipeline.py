from agent_engineer.observability.audit_logger import AuditLogger
from agent_engineer.pipeline import AgentPipeline
def test_pipeline_dangerous_tool_blocks(tmp_path):
    r=AgentPipeline(audit=AuditLogger(tmp_path/"audit.log")).run("帮我退款","issue_refund",500)
    assert not r.success and "deny" in (r.error or "")
def test_pipeline_success(tmp_path):
    r=AgentPipeline(audit=AuditLogger(tmp_path/"audit.log")).run("账单问题","get_order_status",1200)
    assert r.success and r.output is not None and r.cost_usd>0 and r.audit_events>0
