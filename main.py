from Approach2 import *

# Main loop
if __name__ == '__main__':
    try:
        conn = connect_db()
        if conn is None:
            print("Failed to connect to the database. Exiting.")
            exit(1)

        command_list = fetch_all_commands(conn)
        user_input = input("Enter your command: ").strip().lower()

        closest_commands = find_closest_commands(user_input, command_list)

        for closest_command in closest_commands:
            try:
                confirmation = confirm_match(closest_command)
                if confirmation:
                    result = get_command(conn, closest_command)
                    if result:
                        command, description = result
                        # print(f"Command from database: {command}")
                        command_with_values = replace_placeholders(command)
                        # print(f"Command after placeholder replacement: {command_with_values}")
                        try:
                            output = execute_command(command_with_values)
                            print("Command output:")
                            print(output)
                        except Exception as e:
                            print(f"An error occurred: {str(e)}")
                            print("This might be due to permission issues or an invalid directory.")
                    else:
                        print("Command not found in the database.")
                    break
                # If the user said no, the loop will continue to the next closest command
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected. Moving to the next command.")
                continue
        else:
            print("No more close matches found or none accepted.")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting the program.")
        exit(0)
    finally:
        if conn:
            conn.close()