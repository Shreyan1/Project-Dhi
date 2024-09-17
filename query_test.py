"""
Project by Shreyan Basu Ray
Github : https://github.com/Shreyan1/Project-Dhi
LinkedIn : https://linkedin.com/in/shreyanbasuray
Year : 2024

Please feel free to collaborate on this.
Raise issues, PR, anything. I'll review them and fix right away.
--------------------------------------------------------------------
"""


import sqlite3
import subprocess
import re

# Connect to the SQLite database
def connect_db(db_path='SQLiteDB/db_contents.db'):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Query the database to find the appropriate command
def get_command(conn, user_input):
    query = '''
    SELECT command, description FROM "CMD-LIST" WHERE natural_language = ?;
    '''
    cursor = conn.execute(query, (user_input,))
    result = cursor.fetchone()
    return result if result else None

# Replace placeholders with user input
def replace_placeholders(command):
    # Detect placeholders like <filename>, <source>, <destination>, etc.
    placeholders = re.findall(r'<(.*?)>', command)
    
    if placeholders:
        for placeholder in placeholders:
            # Ask the user for each missing parameter
            value = input(f"Which {placeholder} ? Enter here :  ")
            # Replace the placeholder with the user-provided value
            command = command.replace(f"<{placeholder}>", value)
    
    return command

# Execute the command in the terminal
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"

if __name__ == '__main__':
    conn = connect_db()
    if conn is None:
        print("Failed to connect to the database. Exiting.")
        exit(1)

    user_input = input("Enter your command: ").strip().lower()
    result = get_command(conn, user_input)

    if result:
        command, description = result
        print(f"Executing: {description}")
        
        # Replace placeholders like <filename>, <address>, etc.
        command_with_values = replace_placeholders(command)
        
        # Execute command and show output
        output = execute_command(command_with_values)
        print(output)
    else:
        print("Command not found in the database.")
