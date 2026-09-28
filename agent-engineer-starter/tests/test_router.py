from agent_engineer.routing.model_router import ModelRouter
def test_simple_task_light(): assert ModelRouter().route(800,False,1).model_tier=="light"
def test_long_context_standard(): assert ModelRouter().route(2500,False,1).model_tier=="standard"
def test_reasoning_task(): assert ModelRouter().route(1000,True,1).model_tier=="reasoning"
def test_cost_saving():
    r=ModelRouter()
    for _ in range(10): r.route(1000,False,1)
    assert r.cost_summary()["saving_pct"]>80
