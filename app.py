
from langchain.llms import OpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ChatMessageHistory
from typing import Dict
import pandas as pd
import os
from pymongo import MongoClient


from langchain_community.embeddings import OllamaEmbeddings



from langchain_community.chat_message_histories import ChatMessageHistory


from flask import Flask, request, jsonify
import os
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings







# ===================
# SETTIN VARIABLES
# ===================

from variables import *
from chat_history_db_connection import get_mongodb_connection
from agent import *

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key






from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)




@app.route('/process_csv', methods=['POST'])
def process_csv():
    table_name = request.form['table_name']
    file = request.files['csv']

    # Check if the table already exists
    table_exists = check_table_exists(table_name)
    if table_exists:
        # Inform the frontend that the table exists and ask for user confirmation
        return jsonify({
            "message": "Table with that name already exists. Do you want to replace it?",
            "table_exists": True
        })

    # Save the uploaded file temporarily
    filepath = os.path.join("temp", file.filename)
    file.save(filepath)

    # Process the CSV and add it to the database
    message, success = add_database_data(table_name, filepath)

    # Clean up the temporary file
    os.remove(filepath)

    if success:
        return jsonify({"message": message, "table_exists": False})
    else:
        return jsonify({"message": message, "table_exists": False}), 400



@app.route('/delete_and_replace_table', methods=['POST'])
def delete_and_replace_table():
    table_name = request.form['table_name']
    file = request.files['csv']

    # Delete the existing table
    delete_table_with_name(table_name)

    # Save the uploaded file temporarily
    filepath = os.path.join("temp", file.filename)
    file.save(filepath)

    # Process the CSV and add it to the database
    message, success = add_database_data(table_name, filepath)

    # Clean up the temporary file
    os.remove(filepath)

    if success:
        return jsonify({"message": message})
    else:
        return jsonify({"message": message}), 400














def get_class_name(class_type):
    if isinstance(class_type, AIMessage):
        return "AIMessage"
    elif isinstance(class_type, HumanMessage):
        return "HumanMessage"





def invoke_chatbot(session_id, user_message):
    return agent_with_chat_history.invoke(
        {"input": user_message},
        config={"configurable": {"session_id": session_id}},
    )

@app.route('/')
def chat():


    session_id = request.args.get('session_id')
    if not session_id:
        session_id = "defuault"

    raw_history = get_session_history(session_id).messages
    
    # Filter out the summary and format the messages
    chat_history = []
    for message in raw_history:
        if isinstance(message, str):
            continue
        entry = {"type": get_class_name(message), "content": message.content}
        chat_history.append(entry)
    
    # removing summary message
    if (len(chat_history) > history_limit):
        chat_history.pop(0)

    return render_template('chat.html', chat_history=chat_history)





@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message')
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({"response": "Please select/create a session"})

    # Get chatbot response
    chatbot_response = invoke_chatbot(session_id, user_message)
    return jsonify({"response": chatbot_response["output"]})







def insert_pdf_into_vector_store(file_path):

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vector = Neo4jVector.from_documents(
        docs,
        embeddings,
        url=neo4j_url, username=neo4j_username, password=neo4j_password,
        index_name=neo4j_index_name
    )


@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['pdf']
    file_path = os.path.join('data', pdf_file.filename)
    pdf_file.save(file_path)

    insert_pdf_into_vector_store(file_path)

    return jsonify({'message': 'Documents inserted into vector database successfully.'})
    







def get_all_sessions():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['chat_history']
    collection = db['message_store']

    return collection.distinct('SessionId')


@app.route('/get_sessions', methods=['GET'])
def get_sessions():
    return jsonify({ "sessions": get_all_sessions() })









@app.route('/delete_session', methods=['POST'])
def delete_session():
    data = request.json
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({"error": "Session ID is required"}), 400

    # Delete the collection corresponding to the session_id
    history = get_mongodb_connection(session_id).clear()

    return jsonify({"message": "Deleted session"})




if __name__ == '__main__':
    app.run(debug=True)









