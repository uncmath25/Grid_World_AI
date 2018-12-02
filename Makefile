.PHONY: clean
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} \;
	find . -name "*.pyc" -type f -exec rm {} \;

.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: run
run:
	python3 app/_run_grid_world.py
