from neo4j.exceptions import CypherSyntaxError
from utils import cypher_prompt_text, SESSION_ID
from print_color import print
from llm import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from neo4j import GraphDatabase
from langchain_neo4j import Neo4jGraph
from example_provider import select_similar_examples



RETRIES = 3




class Neo4jGPTQuery:
    def __init__(self, url, username, password, retries=2):
        self.driver = GraphDatabase.driver(url, auth=(username, password))
        self.graph = Neo4jGraph(enhanced_schema=True)
        self.llm_chain = self.get_chain()
        self.memory = ChatMessageHistory()
        self.retries = retries

    def get_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [
            (
                "system",
                cypher_prompt_text,
            ),
            ("system", "Schema: \n {schema}"),
            ("system", "Below are some examples ordered by their similarity score with the original query to guide your transformation. Use this as a reference to generate the Cypher query: \n {examples}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "User Question: {question}"),
            ]
        )
        chain = prompt | llm
        chat_with_message_history = RunnableWithMessageHistory(
            chain,
            self.get_memory,
            input_messages_key="question",
            history_messages_key="chat_history",
        )
        return chat_with_message_history 
       
    def get_memory(self, session_id):
        return self.memory
    
    def schema(self):
        self.graph.refresh_schema()
        return self.graph.schema
    
    def query_database(self, neo4j_query, params={}):
        with self.driver.session() as session:
            result = session.run(neo4j_query, params)
            output = [r.values() for r in result]
            output.insert(0, result.keys())
            return output

    def construct_cypher(self, question, history=None) -> str:
        schema = self.schema()
        print(schema)
        similar_examples = select_similar_examples(question)

        print(similar_examples, tag='Similar questions', tag_color='magenta')
        # Used for Cypher healing flows
        if history:
            question += history
        cypher_generated = self.llm_chain.invoke(
            {
                "schema": schema, 
                "examples": similar_examples, 
                "question": question 
            },
            config={"configurable": {"session_id": "none"}}
        )
        return cypher_generated.content
    
    def run(self, question, history=None):
        # Construct Cypher statement
        cypher = self.construct_cypher(question, history)
        print(f"\n{cypher}", tag='Cypher generated', tag_color='blue')
        try:
            return self.query_database(cypher)
        # Self-healing flow
        except CypherSyntaxError as e:
            # If out of retries
            if self.retries <= 0:
              return []
        # Self-healing Cypher flow by
        # providing specific error to GPT-4
            print(f"Retrying...{str(e)}", tag='Cypher error', tag_color='red')
            self.retries -= 1
            return self.run(
                question,
                f""". The query you just build {cypher} returns an error: {str(e)}. 
                Give me a improved query that works without any explanations or apologies"""
            )
        
    def shutdown(self):
        self.driver.close()
    

