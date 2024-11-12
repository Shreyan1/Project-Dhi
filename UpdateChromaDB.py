'''
KNOWLEDGE:
------------
The Chroma database doesn't get saved to a specific file by default when using the in-memory client. 
Instead, it's stored in memory. This means that once the Python script finishes executing, the data is lost unless you explicitly persist it.
To save the Chroma database to disk so you can reuse it across sessions, you need to initialize the Chroma client with a persistence directory. 
When you use Chroma's PersistentClient, it creates a SQLite database file named chroma.sqlite3 to store its data. 
This SQLite file serves as the backend storage for Chroma, containing various tables to manage embeddings, metadata, and other necessary information.
'''

'''
WHEN TO RUN :
--------------
Run UpdateChromaDB.py to add or update the chromadb based on the CMD-LIST.csv in the materials folder
'''

import chromadb
import csv

# Specify file path to update
csv_file_path = 'materials/CMD-LIST.csv'

# Specify a directory for Chroma
persist_directory = "ChromaDB"

# Initialize Chroma client with persistence
client = chromadb.PersistentClient(path=persist_directory)

# Create a collection for commands (or get existing one)
collection = client.get_or_create_collection(name="commands")

def load_commands_from_csv(file_path):
    commands = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            commands.append(row)
    return commands

def populate_db(commands):
    documents = []
    metadatas = []
    ids = []
    for i, cmd in enumerate(commands):
        documents.append(cmd['natural_language'])
        metadatas.append({
            'bash_command': cmd['bash_command']  # Changed to match new column name
        })
        ids.append(str(i))
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Added {len(documents)} commands to the database.")

if __name__ == '__main__':
    commands = load_commands_from_csv(csv_file_path)
    populate_db(commands)
    print(f"Database population complete. Data stored in {persist_directory}")
    