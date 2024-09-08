


from langchain_community.vectorstores import Neo4jVector
from langchain.tools.retriever import create_retriever_tool
from langchain.tools import BaseTool, StructuredTool, Tool, tool
import sqlite3
from langchain.utilities import SQLDatabase


from vector_store import vectorstore
from variables import k_similarity




retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k_similarity})

retriever_tool = create_retriever_tool(
    retriever,
    "kraftmarked_kunnskap",
    "Søk for informasjon fra domenekunnskap. Hvis brukeren sier du skal bruke domenekunnskap, så bruk dette verktøyet!",
)









@tool
def database_search(query: str) -> str:
    "Search the database for data. Use this tool if the user asks to use the database. The user will provide the name of the table to search"
    try:
        db_chain = SQLDatabaseChain.from_llm(llm, sql_db, verbose=True)
    except:
        return str("failed database search")
    return str(db_chain.run(query))


conn = sqlite3.connect('database.db', check_same_thread=False)
sql_db = SQLDatabase.from_uri("sqlite:///database.db")


def check_table_exists(table_name):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name=?;
    """, (table_name,))
    result = cursor.fetchone()
    return result is not None


def delete_table_with_name(table_name):
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    conn.commit()


def add_database_data(table_name, filepath):
    df = pd.read_csv(filepath)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    return f"Table '{table_name}' added to the database successfully.", True







tools =  [retriever_tool, database_search]





