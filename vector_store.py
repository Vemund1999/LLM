
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
import os



from variables import *


os.environ["OPENAI_API_KEY"] = openai_api_key


embeddings = OpenAIEmbeddings()
# embeddings = OllamaEmbeddings()


# accessing domain data
vectorstore = Neo4jVector.from_existing_index(
    embeddings,
    url=neo4j_url,
    username=neo4j_username,
    password=neo4j_password,
    index_name=neo4j_index_name
    # keyword_index_name=keyword_index_name,
    # search_type="hybrid"
)





