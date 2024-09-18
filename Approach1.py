"""
Project by Shreyan Basu Ray
Github : https://github.com/Shreyan1/Project-Dhi
LinkedIn : https://linkedin.com/in/shreyanbasuray
Year : 2024

Please feel free to collaborate on this.
Raise issues, PR, anything. I'll review them and fix right away.
--------------------------------------------------------------------
"""


## APPROACH 1

import sqlite3
import subprocess
import re

from difflib import get_close_matches

# Connect to the SQLite database
def connect_db(db_path='SQLiteDB/db_contents.db'):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Fetch all natural language commands from the database
def fetch_all_commands(conn):
    query = '''
    SELECT natural_language FROM "CMD-LIST";
    '''
    cursor = conn.execute(query)
    return [row[0] for row in cursor.fetchall()]

# Query the database to find the appropriate command
def get_command(conn, natural_language):
    query = '''
    SELECT command, description FROM "CMD-LIST" WHERE natural_language = ?;
    '''

    cursor = conn.execute(query, (natural_language,))
    result = cursor.fetchone()
    return result if result else None

# Replace placeholders with user input
def replace_placeholders(command):
    # Detect placeholders like <filename>, <source>, <destination>, etc.
    placeholders = re.findall(r'<(.*?)>', command)
    
    if placeholders:
        for placeholder in placeholders:
            # Ask the user for each missing parameter
            value = input(f"Enter {placeholder}: ")
            # Replace the placeholder with the user-provided value
            command = command.replace(f"<{placeholder}>", value)
    
    return command

# Execute the command in the terminal
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, 
                                check=True, text=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"

# Match user input to the closest commands using fuzzy matching
def find_closest_commands(user_input, command_list):
    return get_close_matches(user_input, 
                             command_list, 
                             n=5, 
                             cutoff=0.6)

# Confirm if the closest match is what the user intended
def confirm_match(closest_command):
    confirmation = input(f"Closest match found: '{closest_command}'. Is this correct? (y/n): ").strip().lower()
    return confirmation == 'y'


if __name__ == '__main__':
    conn = connect_db()
    if conn is None:
        print("Failed to connect to the database. Exiting.")
        exit(1)

    command_list = fetch_all_commands(conn)
    user_input = input("Enter your command: ").strip().lower()
    closest_commands = find_closest_commands(user_input, command_list)

    for closest_command in closest_commands:
        if confirm_match(closest_command):
            result = get_command(conn, closest_command)
            
            if result:
                command, description = result
                print(f"Executing: {command}")
                command_with_values = replace_placeholders(command)
                output = execute_command(command_with_values)
                print(output)
            else:
                print("Command not found in the database.")
            break
    else:
        print("No more close matches found or none accepted.")
