#!/bin/sh

echo ""
echo "Pass 'start' to start production code"
echo "          Or              "
echo "docker exec -it <container_id> bash"
echo "in new terminal."
echo ""

if [ -z "$1" ]; then
    echo "Not enough arguments passed";
    exit 0
elif [ $1 == "start" ]; then
    # Add main code
    sleep 99999999;
elif [ $1 == "hold" ]; then
    sleep 99999999;
else
    echo "Argument not recognized";
fi