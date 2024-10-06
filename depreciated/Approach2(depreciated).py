"""
Project by Shreyan Basu Ray
Github : https://github.com/Shreyan1/Project-Dhi
LinkedIn : https://linkedin.com/in/shreyanbasuray
Year : 2024

Please feel free to collaborate on this.
Raise issues, PR, anything. I'll review them and fix right away.
--------------------------------------------------------------------
"""

## APPROACH 2

# from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
# import folder_handling as fh

# import torch
import sqlite3
import numpy as np

import re
import subprocess

# Suppressing the clean_up_tokenization_spaces issue warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#-----------------------------------------------#

# # Load the transformer model and tokenizer (PyTorch)
# tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', clean_up_tokenization_spaces=True)
# model = AutoModel.from_pretrained('bert-base-uncased')

# Load the Universal Sentence Encoder
sentence_encoder = SentenceTransformer("all-MiniLM-L6-v2")

# # Function to convert text to embedding using transformer model (PyTorch)
# def get_embedding(text):
#     inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     # Squeeze out the batch dimension and reduce it to 2D (batch_size, embedding_dim)
#     return outputs.last_hidden_state.mean(dim=1).squeeze(0).numpy()

#-----------------------------------------------#

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
    query = 'SELECT natural_language FROM "CMD-LIST";'
    cursor = conn.execute(query)
    return [row[0] for row in cursor.fetchall()]

# Query the database to find the appropriate command
def get_command(conn, natural_language):
    query = 'SELECT command, description FROM "CMD-LIST" WHERE natural_language = ?;'
    cursor = conn.execute(query, (natural_language,))
    result = cursor.fetchone()
    return result if result else None

# Function to get embeddings using the Universal Sentence Encoder
def get_embedding(text):
    return sentence_encoder.encode([text])[0]

# Replace placeholders with user input
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

#-----------------------------------------------#

# Execute the command in the terminal
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

# Match user input to the closest commands using Universal Sentence Encoder embeddings
def find_closest_commands(user_input, command_list):
    user_embedding = get_embedding(user_input)
    command_embeddings = np.array([get_embedding(command) for command in command_list])

    similarities = cosine_similarity([user_embedding], command_embeddings)[0]
    best_matches = np.argsort(similarities)[::-1][:6]  # Get top 6 closest commands
    return [(command_list[idx], similarities[idx]) for idx in best_matches]


# Confirm if the closest match is what the user intended
def confirm_match(closest_command, similarity):
    while True:
        try:
            confirmation = input(f"Closest match found: '{closest_command}' (Similarity: {(similarity*100):.2f}%). \nIs this correct? (y/n ? Press q to quit): ")
        
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

#-----------------------------------------------#

# if __name__ == '__main__':
#     conn = connect_db()
#     if conn is None:
#         print("Failed to connect to the database. Exiting.")
#         exit(1)

#     try:
#         command_list = fetch_all_commands(conn)
#         user_input = input("Enter your command: ").strip().lower()

#         closest_commands = find_closest_commands(user_input, command_list)

#         for closest_command, similarity in closest_commands:
#             try:
#                 if confirm_match(closest_command, similarity):
#                     result = get_command(conn, closest_command)
#                     if result:
#                         command, description = result
#                         print(f"Command from database: {command}")
#                         print(f"Description: {description}")
                        
#                         # Replace placeholders and execute the command
#                         command_with_values = replace_placeholders(command)
#                         print(f"Command after placeholder replacement: {command_with_values}")
                        
#                         output = execute_command(command_with_values)
#                         print("Command output:")
#                         print(output)
#                     else:
#                         print("Command not found in the database.")
#                     break
#             except KeyboardInterrupt:
#                 print("\nKeyboard interrupt detected. Moving to the next command.")
#                 continue
#         else:
#             print("No more close matches found or none accepted.")

#     except KeyboardInterrupt:
#         print("\nKeyboard interrupt detected. Exiting the program.")
#     finally:
#         if conn:
#             conn.close()