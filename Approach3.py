"""
Project by Shreyan Basu Ray
Github : https://github.com/Shreyan1/Project-Dhi
LinkedIn : https://linkedin.com/in/shreyanbasuray
Year : 2024

Please feel free to collaborate on this.
Raise issues, PR, anything. I'll review them and fix right away.
--------------------------------------------------------------------
"""

## APPROACH 3 : USING VECTORDB APPROACH USING CHROMADB

'''
Run UpdateChromaDB.py to add or update the chromadb based on the CMD-LIST.csv in the materials folder
'''

import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

persist_directory = "ChromaDB"

# Initialize Chroma client with persistence and get the collection
client = chromadb.PersistentClient(path=persist_directory)
collection = client.get_collection(name="commands")

# Initialize the sentence transformer for encoding
sentence_encoder = SentenceTransformer("all-MiniLM-L6-v2")

def find_closest_commands(user_input, n=6):
    results = collection.query(
        query_texts=[user_input],
        n_results=n
    )
    return list(zip(results['documents'][0], 
                    results['metadatas'][0], 
                    results['distances'][0]))

def replace_placeholders(command):
    placeholders = re.findall(r'<(.*?)>', command)
    if placeholders:
        for placeholder in placeholders:
            if placeholder == "foldername":
                value = input(f"Enter {placeholder} [Note: for any top level directories, please declare as eg - /home, /var etc.] : ")
            else:
                value = input(f"Enter {placeholder}: ")
            command = command.replace(f"<{placeholder}>", value)
    return command

def execute_command(command):
    try:
        result = subprocess.run(command, 
                                shell=True,
                                check=True, text=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"

def confirm_match(closest_command, similarity):
    while True:
        try:
            confirmation = input(f"Closest match found: '{closest_command}' (Similarity: {(1-similarity)*100:.2f}%). \nIs this correct? (y/n ? Press q to quit): ")
        
            if confirmation.lower() == 'y':
                return True
            elif confirmation.lower() == 'n':
                return False
            elif confirmation.lower() == 'q':
                print("Exiting the program.")
                exit(0)
            else:
                print("Invalid input. Please enter 'y' for yes, 'n' for no, or 'q' to quit.")
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting the program.")
            exit(0)


# --------------------------------------------------------------
# if __name__ == '__main__':
#     try:
#         while True:
#             user_input = input("Enter your command: ").strip().lower()
#             closest_commands = find_closest_commands(user_input)
#             for natural_language, metadata, distance in closest_commands:
#                 try:
#                     if confirm_match(natural_language, distance):
#                         command = metadata['command']
#                         description = metadata['description']
#                         print(f"Command from database: {command}")
#                         print(f"Description: {description}")
                        
#                         command_with_values = replace_placeholders(command)
#                         print(f"Command after placeholder replacement: {command_with_values}")
                        
#                         output = execute_command(command_with_values)
#                         print("Command output:")
#                         print(output)
#                         break
#                 except KeyboardInterrupt:
#                     print("\nKeyboard interrupt detected. Moving to the next command.")
#                     continue
#             else:
#                 print("No more close matches found or none accepted.")
#     except KeyboardInterrupt:
#         print("\nKeyboard interrupt detected. Exiting the program.")
