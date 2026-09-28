from agent_engineer.fallback.fallback_orchestrator import FallbackLevel,FallbackOrchestrator
def test_dangerous_tool_goes_human(): assert FallbackOrchestrator(2).decide("dangerous_tool",0)==FallbackLevel.HUMAN
def test_schema_retry_then_safe():
    f=FallbackOrchestrator(2)
    assert f.decide("schema_invalid",0)==FallbackLevel.RETRY
    assert f.decide("schema_invalid",1)==FallbackLevel.RETRY
    assert f.decide("schema_invalid",2)==FallbackLevel.SAFE_REPLY
