# CommandAndControl/Makefile
.PHONY: run test clean

# Run the Flask server in dev mode (uses your venv’s python)
run:
	@source env/bin/activate && \
	    FLASK_APP=server.py FLASK_ENV=development flask run

# One-liner test runner (green dots or bust)
test:
	@source env/bin/activate && \
	    python -m pytest -q

# Toss compiled files /pytest cache
clean:
	find . -type f -name '*.py[co]' -delete
	rm -rf __pycache__ .pytest_cache

