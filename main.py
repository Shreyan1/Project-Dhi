from Approach3 import *

if __name__ == '__main__':
    try:
        while True:
            user_input = input("Enter your command: ").strip().lower()
            closest_commands = find_closest_commands(user_input)
            for natural_language, metadata, distance in closest_commands:
                try:
                    if confirm_match(natural_language, distance):
                        command = metadata['command']
                        description = metadata['description']
                        print(f"Command from database: {command}")
                        print(f"Description: {description}")
                        
                        command_with_values = replace_placeholders(command)
                        print(f"Command after placeholder replacement: {command_with_values}")
                        
                        output = execute_command(command_with_values)
                        print("Command output:")
                        print(output)
                        break
                except KeyboardInterrupt:
                    print("\nKeyboard interrupt detected. Moving to the next command.")
                    continue
            else:
                print("No more close matches found or none accepted.")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting the program.")
