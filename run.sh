#!/bin/bash

# Making sure script is sourced, not executed for venv activation
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Error: This script must be sourced. Run it as either:"
    echo "1)   source run.sh [--options] , or"
    echo "2)   . run.sh [--options]"
    exit 1
fi

PROJENV="dhienv"
DEBUG=false
SILENT=false
SETUP_COMPLETE=false  # Flag to track setup completion

# Check for debug and silent flags before other parameters
for arg in "$@"; do
    if [[ "$arg" == "--debug" || "$arg" == "-D" ]]; then
        DEBUG=true
    elif [[ "$arg" == "--silent" || "$arg" == "-S" ]]; then
        SILENT=true
    fi
done

# Modify check functions to use decho
decho() {
    if [[ "$DEBUG" == true ]]; then
        echo "$@"
    fi
}

# Add debug flag to help message
show_help() {
    echo "Usage: source run.sh [OPTIONS]"
    echo "A script to manage Python virtual environment and dependencies setup."
    echo ""
    echo "Options:"
    echo "  -H, --help        Display this help message and exit"
    echo "  -V, --venv        Create a new virtual environment (if not exists) and/or"
    echo "                    activate it interactively"
    echo "  -I, --install     Install Python packages from requirements.txt in the"
    echo "                    current virtual environment"
    echo "  -S, --silent      Non-interactive mode: automatically create venv (if needed),"
    echo "                    activate it, and install all dependencies without prompts"
    echo "  -D, --debug       Enable debug mode to show detailed execution messages"
    echo ""
    echo "Some Examples:"
    echo "  source run.sh --venv          # Interactive setup of virtual environment"
    echo "  source run.sh -S              # Automatic setup of everything"
    echo "  source run.sh -V -D           # Setup venv with debug messages"
    echo "  . run.sh --silent --debug     # Automatic setup with debug messages"
    return 0
}

check_os() {
    decho "Checking OS..."
    if [[ "$(uname)" != "Linux" ]]; then
        echo "Error: The OS you are using is not supported. This only works on Linux."
        return 1
    else
        decho "|| OS is supported."
    fi
}

check_python3() {
    decho "Checking installed Python Version..."
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is not installed. Please install Python 3.10 or higher and try again."
        return 1
    fi
    
    version=$(python3 -V 2>&1)
    decho "|| Python version: $version"
    
    if [[ "$(echo $version | cut -d. -f1-2)" < "3.10" ]]; then
        echo "Error: Python 3.10 or higher is required. Your version is $version."
        echo "|| Please install Python 3.10 or higher and try again."
        return 1
    fi
}

prechecks() {
    decho "Running prechecks..."
    if ! check_os || ! check_python3; then
        return 1
    fi
    decho "Prechecks passed."
    return 0
}

# Executing the prechecks
prechecks

# Checks and installs requirements
install_pip() {
    if [[ ! -f "requirements.txt" ]]; then
        echo "Error: 'requirements.txt' not found in the current directory."
        return 1
    fi
    
    decho "requirements.txt found in the current directory"
    
    echo "Installing pip dependencies..."
    if ! pip install -r requirements.txt; then
        echo "Error: Failed to install dependencies from requirements.txt"
        return 1
    fi
    echo "Pip dependencies installed successfully."
    return 0
}

# Activates the virtual environment
activate_venv() {
    if [[ "$SILENT" == true ]]; then
        source "$PROJENV/bin/activate"
        echo "Virtual environment activated."
        if ! install_pip; then
            return 1
        fi
        return 0
    fi

    local response
    local attempts=0

    while [[ $attempts -lt 3 ]]; do
        read -r -p "Do you want to activate the virtual environment? (y/n) " response
        response=${response,,}
        response=$(echo "$response" | tr -d '[:space:]')

        if [[ "$response" == "y" ]]; then
            source "$PROJENV/bin/activate"
            echo "Virtual environment activated successfully."
            echo "Run command -> deactivate ; to deactivate the virtual environment manually"
            echo ""
            install_pip
            return 0
        elif [[ "$response" == "n" ]]; then
            echo "Skipped activating virtual environment."
            echo "Run: source $PROJENV/bin/activate to activate the virtual environment manually later."
            return 0
        fi

        echo "Invalid input. Please enter 'Y/N' or 'y/n'."
        ((attempts++))
    done

    echo "Maximum attempts reached. Defaulting to 'n'."
    echo "Skipped activating virtual environment."
}


create_venv() {
    if [[ "$SILENT" == true ]]; then
        echo "Creating virtual environment '$PROJENV'..."
        if ! python3 -m venv $PROJENV; then
            echo "Failed to create virtual environment."
            return 1
        fi
        echo "Virtual environment '$PROJENV' created successfully."
        if ! activate_venv; then
            return 1
        fi
        return 0
    fi
    
    local response
    local attempts=0

    while [[ $attempts -lt 3 ]]; do
        read -r -p "Virtual environment '$PROJENV' does not exist. Do you want to create it? (y/n) " response
        response=${response,,}  # Convert to lowercase
        response=$(echo "$response" | tr -d '[:space:]')  # Remove whitespace

        if [[ "$response" == "y" ]]; then
            echo "|| Creating virtual environment '$PROJENV'..."
            python3 -m venv $PROJENV
            echo "|| Virtual environment '$PROJENV' created successfully."
            activate_venv
            return 0
        elif [[ "$response" == "n" ]]; then
            echo "Skipped creating virtual environment."
            return 0
        fi

        echo "|| Invalid input. Please enter 'Y/N' or 'y/n'."
        ((attempts++))
    done

    echo "Maximum attempts reached. Defaulting to 'n'."
    echo "|| Skipped creating virtual environment."
}

check_and_install_missing_packages() {
    local missing_packages=()
    while IFS= read -r package; do
        # Skip empty lines and comments
        [[ -z "$package" || "$package" =~ ^#.*$ ]] && continue
        
        # Extract package name without version
        package_name=$(echo "$package" | cut -d'=' -f1)
        
        if ! pip show "$package_name" &>/dev/null; then
            missing_packages+=("$package")
        fi
    done < requirements.txt

    if [ ${#missing_packages[@]} -ne 0 ]; then
        echo "The following packages are missing and will be installed:"
        printf '%s\n' "${missing_packages[@]}"
        for package in "${missing_packages[@]}"; do
            if ! pip install "$package"; then
                echo "Warning: Failed to install $package. Attempting to install without version specification."
                package_name=$(echo "$package" | cut -d'=' -f1)
                if ! pip install "$package_name"; then
                    echo "Error: Failed to install $package_name"
                    return 1
                fi
            fi
        done
        echo "All missing packages have been installed."
    else
        echo "All required packages are already installed."
    fi
    return 0
}

run_python_script() {
    if ! prechecks; then
        echo "Error: System requirements not met. Cannot run Project Dhi."
        return 1
    fi

    if [[ ! -f "main.py" ]]; then
        echo "Error: main.py not found in current directory."
        return 1
    fi

    echo "Checking for missing packages..."
    if ! check_and_install_missing_packages; then
        echo "Error: Failed to install missing packages. Cannot run Project Dhi."
        return 1
    fi

    echo "Running Project Dhi..."
    python3 main.py
    decho "Python script executed."
    return 0
}

setup_and_run() {
    # Run prechecks first
    if ! prechecks; then
        echo "Prechecks failed. Aborting setup."
        return 1
    fi

    # Handle virtual environment setup
    if [[ -d "$PROJENV" ]]; then
        echo "Virtual environment '$PROJENV' already exists."
        if ! activate_venv; then
            return 1
        fi
    else
        if ! create_venv; then
            return 1
        fi
    fi

    SETUP_COMPLETE=true

    # Ask user if they want to start Project Dhi
    local response
    local attempts=0

    echo ""
    echo "Setup completed successfully!"
    while [[ $attempts -lt 3 ]]; do
        read -r -p "Do you want to start Project Dhi? (y/n) " response
        response=${response,,}
        response=$(echo "$response" | tr -d '[:space:]')

        if [[ "$response" == "y" ]]; then
            if [[ ! -f "main.py" ]]; then
                echo "Error: main.py not found in current directory."
                return 1
            fi
            echo "Starting Project Dhi..."
            python3 main.py
            decho "Python script executed."
            return 0
        elif [[ "$response" == "n" ]]; then
            echo "Setup completed. You can run Project Dhi later using: source run.sh"
            return 0
        fi

        echo "Invalid input. Please enter 'Y/N'."
        ((attempts++))
    done

    echo "Maximum attempts reached. Skipping Project Dhi startup."
    return 0
}

# Check if a parameter is passed
if [[ "$1" == "--help" || "$1" == "-H" ]]; then
    show_help
    return 0

elif [[ "$1" == "--venv" || "$1" == "-V" ]]; then
    if [[ -d "$PROJENV" ]]; then
        echo "Virtual environment '$PROJENV' already exists."
        activate_venv
    else
        create_venv
    fi

elif [[ "$1" == "--install" || "$1" == "-I" ]]; then
    install_pip

elif [[ "$1" == "--silent" || "$1" == "-S" ]]; then
    setup_and_run

elif [[ "$#" -gt 0 && "$1" != "--debug" && "$1" != "-D" ]]; then
    echo "Error: Unsupported parameter '$1'"
    echo "Use --help or -H to display the help message."
    return 1

else
    # No flags provided, just run the Python script with minimal checks
    run_python_script
fi