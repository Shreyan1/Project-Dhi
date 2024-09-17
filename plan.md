# Project Dhi : Plan

### Idea :
- Execute commands in Natural Language on your terminal
- Primarily Linux Based

## Things to do :
- First start out with basic commands of Linux and check whether it is working fine
- Create a sqlite db with all the descriptions
- ### Contents of the sqlite db :
        - id
        - natural language
        - command
        - description
- The natural language input by the user will be checked for the query, if it is matching, it will fetch that particular command and execute it on the terminal
- this is like the basic idea, we can optimise it far far more and make it the best thing

## SQLite Starter Content :
-  

## Techstack to be used "
- Python
    - now being used for sqlite connection and all but not really sure how much delay python would cause compared to rust, so might change later
    - to handle the commands and the user input
    - will be required for natural language interpretation
- Rust
    - will be used to communicate with the terminal
    - i'm aware of the pros and cons but I've read multiple Medium blogs to know that Rust can be a pain in the ass
- SQLite
    - 


-------------------------------------------------------

# NLP Implementation : 

To implement a Natural Language Processing (NLP) system that can understand user input and match it to the closest natural language command in the database, we need to take the following steps:

### Approach:

- Text Preprocessing: Clean the user input to make it easier to compare with the commands in the database.
- Similarity Measure: Use a method to measure similarity between the user's input and the commands in the database. We can start with a basic approach, such as:
    - Cosine Similarity or Jaccard Similarity on tokenized inputs.
- Levenshtein Distance (edit distance).
- More advanced approaches like word embeddings (e.g., spaCy, transformers) can be implemented if needed.
- Rank the Matches: Rank the possible matches from the database and choose the closest one.
- Handle Fuzzy Matching: If no exact match is found, suggest the closest matches or handle errors gracefully.

### Implementation:
We can start by using a simple similarity metric, like Levenshtein Distance, which calculates the number of edits (insertions, deletions, or substitutions) needed to transform one string into another. This method works well for fuzzy matching.

For a more sophisticated NLP solution, we can later integrate libraries like spaCy or fuzzywuzzy OR TRANSFORMERS !!

--------------------

## Current Output Status :

Enter your command: remove file
Closest match found: 'move file'. Is this correct? (y/n): n
Closest match found: 'remove directory'. Is this correct? (y/n): n
Closest match found: 'delete file'. Is this correct? (y/n): y
Executing: rm <filename>
Enter filename: deleteme.txt