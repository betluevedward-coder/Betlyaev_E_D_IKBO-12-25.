.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest tests/

run:
	python3 -m src.nuget_viz.main $(ARGS)

clean:
	rm -rf __pycache__ src/nuget_viz/__pycache__ tests/__pycache__