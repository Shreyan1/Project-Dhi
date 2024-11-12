import chromadb
import csv

# Specify file path to update
csv_file_path = 'materials/paired_nl_bash.csv'

# Specify a directory for Chroma
persist_directory = "ChromaDB2"

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
            'bash_command': cmd['bash_command']
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
