.PHONY: install verify cleanup monitor test
install:
	bash scripts/install.sh
verify:
	bash scripts/verify.sh
cleanup:
	bash scripts/cleanup.sh
monitor:
	python scripts/monitor_gpu.py
test:
	pytest -v tests/
