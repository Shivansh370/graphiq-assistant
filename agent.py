from utils import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
import streamlit as st
from utils import  loan_prompt, metadata_prompt, SESSION_ID
from neo4j_gpt_query import Neo4jGPTQuery
from llm import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from print_color import print

 



memory = ChatMessageHistory()

def get_memory(session_id):
    return memory




class Agent:
    def __init__(self):
        
        self.chat_with_message_history = None
        self.neo4j_gpt = Neo4jGPTQuery(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            retries=3
        )

    
    def generate_response(self, question):
        if not self.chat_with_message_history:
            return ""

        context = self.neo4j_gpt.run(question)
        print(context, tag='Context', tag_color='yellow', color='yellow')
        response = self.chat_with_message_history.invoke(
            {
                "context": context, 
                "question": question
            },  
            config={"configurable": {"session_id": SESSION_ID}}
        ).content
        print(response, tag='Response', tag_color='green', color='green')
        return response
    
    def select_prompt_from_selection(self):
        

        if st.session_state.data_selection == 'Loss Draft Loan Q&A':
            agent_prompt_file = loan_prompt
        elif st.session_state.data_selection == 'Report Metadata Q&A':
            agent_prompt_file = metadata_prompt


        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                agent_prompt_file,
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("system", "Use this Context to answer the question: {context}"),
            ("human", "The User Question is: {question}"),
        ]
        )
        llm_chain = prompt | llm 

        self.chat_with_message_history = RunnableWithMessageHistory(
                    llm_chain,
                    get_memory,
                    input_messages_key="question",
                    history_messages_key="chat_history",
                )
    





agent = Agent()







