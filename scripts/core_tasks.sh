#!/bin/bash

pyfiglet BULLETIN - TIMELOOP

echo "Running core.tasks..."

python3 -m core.tasks > /dev/null 2>&1 &

echo "background task activated.."

