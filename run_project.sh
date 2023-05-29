#!/bin/bash

# Start the first process
uvicorn api:app --reload --host 0.0.0.0 &
# Start the second process
flask --app main run --debug --port 6000 --host 0.0.0.0 &
# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
