

from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory




from tools import tools
from variables import openai_api_key, model, mongodb_url, history_limit
from chat_history_db_connection import get_mongodb_connection




llm = ChatOpenAI(
    api_key=openai_api_key,
    model=model
)



# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")
"""
prompt innhold:

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            promt_content,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
"""











# history er chat_message history. så må manipulere den
def summerize_history(session_id):

    history = get_mongodb_connection(session_id)
    history_messages = history.messages
    
    # checking if messages should be summerized
    if len(history_messages) <= history_limit:
        return history





 
    # summerizing the messages using an llm
    llm = Ollama(model="llama2")

    summerize_prompt = "Distill the above chat messages into a single summary message. Include as many specific details as you can."
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat"),
            (
                "user",
                summerize_prompt,
            ),
        ]
    )
    history_up_to_limit = history_messages[:-history_limit] 

    summarization_chain = summarization_prompt | llm
    summary_message = summarization_chain.invoke({"chat": history_up_to_limit})


    # reformating history
    history_after_limit = history_messages[-history_limit:] 

    history.clear()
    history.add_ai_message(summary_message)
    history.add_messages(history_after_limit)

    return history






            
        







def get_session_history(session_id: str) -> BaseChatMessageHistory:


    history = MongoDBChatMessageHistory(
        connection_string=mongodb_url,  
        session_id=session_id,
    )

    # summerze chat history
    history = summerize_history(session_id)

    return history




agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history, 
    input_messages_key="input",
    history_messages_key="chat_history",
)


