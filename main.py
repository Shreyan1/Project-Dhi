from Approach2 import *

# Main loop
if __name__ == '__main__':
    conn = connect_db()
    if conn is None:
        print("Failed to connect to the database. Exiting.")
        exit(1)

    try:
        command_list = fetch_all_commands(conn)
        user_input = input("Enter your command: ").strip().lower()

        closest_commands = find_closest_commands(user_input, command_list)

        for closest_command, similarity in closest_commands:
            try:
                if confirm_match(closest_command, similarity):
                    result = get_command(conn, closest_command)
                    if result:
                        command, description = result
                        print(f"Command from database: {command}")
                        print(f"Description: {description}")
                        
                        # Replace placeholders and execute the command
                        command_with_values = replace_placeholders(command)
                        print(f"Command after placeholder replacement: {command_with_values}")
                        
                        output = execute_command(command_with_values)
                        print("Command output:")
                        print(output)
                    else:
                        print("Command not found in the database.")
                    break
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected. Moving to the next command.")
                continue
        else:
            print("No more close matches found or none accepted.")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting the program.")
    finally:
        if conn:
            conn.close()