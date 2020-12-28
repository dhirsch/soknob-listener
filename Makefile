debug:
	echo "Running with reload"
	poetry run uvicorn main:app --host 0.0.0.0 --port 4999 --reload
