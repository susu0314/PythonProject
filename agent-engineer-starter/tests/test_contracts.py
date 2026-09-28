from agent_engineer.contracts.structured_contract import validate_ticket_output
def test_valid_output():
    ok,fb,p=validate_ticket_output('{"category":"billing","confidence":0.9,"reason":"账单异常","priority":"high"}'); assert ok and fb is None and p is not None
def test_invalid_enum():
    ok,fb,p=validate_ticket_output('{"category":"unknown","confidence":0.9,"reason":"x"}'); assert not ok and "category" in fb and p is None
def test_confidence_out_of_range():
    ok,fb,_=validate_ticket_output('{"category":"billing","confidence":1.5,"reason":"x"}'); assert not ok and "confidence" in fb
def test_json_parse_error():
    ok,fb,_=validate_ticket_output("not-a-json"); assert not ok and "JSON" in fb
