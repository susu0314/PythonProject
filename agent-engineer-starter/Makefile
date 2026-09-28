.PHONY: install demo troubleshoot test clean
install:
	pip install -e ".[dev]"
demo:
	python -m examples.demo_ticket_classification
troubleshoot:
	python -m examples.demo_troubleshooting
test:
	pytest -v --cov=agent_engineer
clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage audit.log
	find . -type d -name __pycache__ -exec rm -rf {} +
