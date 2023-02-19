#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No argument provided"
    exit 1
fi

echo "$1" > token
echo "Token saved to 'token'"
