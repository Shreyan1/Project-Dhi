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
    # If any other parameter is passed, show an error
    echo "Error: Unsupported parameter '$1'"
    echo "Use --help or -H to display the help message."
    exit 1
fi

# Check if the OS is Linux
if [[ "$(uname)" != "Linux" ]]; then
    echo "Error: The OS you are using is not supported. This script only works on Linux."
    exit 1
fi

# If everything is fine, run the Python script
python3 main.py
