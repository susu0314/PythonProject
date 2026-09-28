from agent_engineer.safety.safety_guardrail import GuardrailPolicy,SafetyGuard
def test_deny_list_blocks():
    ok,msg=SafetyGuard().check_tool("delete_volume"); assert not ok and "deny" in msg
def test_allow_list_permits(): assert SafetyGuard().check_tool("get_order_status")[0]
def test_rate_limit():
    g=SafetyGuard(GuardrailPolicy(rate_limits={"get_order_status":2}))
    assert g.check_tool("get_order_status")[0] and g.check_tool("get_order_status")[0]
    ok,msg=g.check_tool("get_order_status"); assert not ok and "速率限制" in msg
def test_pii_redaction():
    out=SafetyGuard().redact_outbound("手机号 13812345678，邮箱 a@b.com，key sk-ant-abcdefghijklmnopqrst")
    assert "13812345678" not in out and "a@b.com" not in out and "sk-ant-abcdefghijklmnopqrst" not in out
