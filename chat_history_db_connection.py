from langchain_mongodb import MongoDBChatMessageHistory
from variables import mongodb_url



def get_mongodb_connection(session_id):

    history = MongoDBChatMessageHistory(
        connection_string=mongodb_url,  
        session_id = session_id,
    )
    return history

