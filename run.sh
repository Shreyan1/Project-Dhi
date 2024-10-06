#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: ./run_main.sh [OPTION]"
    echo "Options:"
    echo "  -H, --help      Show this help message"
    exit 0
}

# Check if a parameter is passed
if [[ "$1" == "--help" || "$1" == "-H" ]]; then
    show_help
elif [[ "$#" -gt 0 ]]; then
    echo "Error: Unsupported parameter '$1'"
    echo "Use --help or -H to display the help message."
    exit 1
fi

# Check if the OS is Linux
if [[ "$(uname)" != "Linux" ]]; then
    echo "Error: The OS you are using is not supported. This script only works on Linux."
    exit 1
fi

echo "Running Python script..."
error_output=$(python3 Approach3.py 2>&1)
exit_status=$?  # Capture the exit status of the Python script

echo "$error_output"  # Display output

if [[ $exit_status -ne 0 ]]; then
    if echo "$error_output" | grep -q "ModuleNotFoundError"; then
        echo ""
        echo "Error: One or more modules are missing."
        echo "Please create/activate a virtual environment and/or run: pip install -r requirements.txt"
    else
        echo "An error occurred while running the Python script:"
        echo "$error_output"
    fi
    exit 1
fi

echo "Python script executed successfully."
