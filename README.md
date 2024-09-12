# Setup 

## Prerequisite
- You have docker installed
- You have a openai API key
- You have a langchain API key

## Variables
- Edit the variables.py file to whatever values you want


## Setup project
- Run the docker_setup.sh

This will make two docker containers
- One for a vector store database in neo4j
- Another for a chat history database in mongodb

<br />

- Execute the following command in the neo4j browser at http://localhost:7474/browser/:
```
CREATE VECTOR INDEX vector IF NOT EXISTS
FOR (m:Chunk)
ON m.embedding
OPTIONS {indexConfig: {
 `vector.dimensions`: 1536,
 `vector.similarity_function`: 'cosine'
}}
```
The dimensions value is specifically for gpt-3.5-turbo.

If you change the model, you also have to change the dimensions.

- Run: `pip install -r requirements.txt`



## Run
- Run the app.py file
- Go to http://localhost:5000



# Capabilities of this project
- Runs an LLM
- Has a web-gui for interracting with the LLM
- The LLM has memory, chat history is saved
- Chat history can be freely limited. The LLM will summerize messages that are far enough behind in the log. This is done by using a second LLM (llama2)
- A user can create different sessions with the LLM
- A user can give domain-knowledge by providing pdf-files
- The LLM can be given csv files, which it can read by saving the data to a sql-lite database

# Images of the application GUI
![2024-09-08_13-05](https://github.com/user-attachments/assets/5c1a2889-c61b-469f-a86b-03f344a3df75)

![2024-09-08_13-06](https://github.com/user-attachments/assets/950d2598-e1d1-4e91-b011-fd9792a02dae)

![2024-09-08_13-06_1](https://github.com/user-attachments/assets/d15a9b97-3915-4828-bdea-5bb54333454b)

![2024-09-08_13-06_2](https://github.com/user-attachments/assets/c650368c-2a7b-404c-a11d-9df17193cea1)











