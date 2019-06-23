.PHONY: install clean flake test run

install:
	@echo "*** Installing necessary requirements ***"
	pip3 install -r requirements.txt

clean:
	@echo "*** Cleaning unnecessary caches ***"
	@rm -rf `find . -name __pycache__`
	rm -rf .pytest_cache

flake:
	@echo "*** Linting python code ***"
	flake8 . --ignore="E501"

test:
	@echo "*** Running tests ***"
	# pytest .

run:
	@echo "*** Running simulation ***"
	python3 app/_run_grid_world.py
