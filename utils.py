import argparse
import sys
from dotenv import load_dotenv
import os
from uuid import uuid4
import streamlit as st

# Initialize session ID using st.session_state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

SESSION_ID = st.session_state.session_id

load_dotenv()

AZURE_ENDPOINT = os.environ["AZURE_ENDPOINT"]
API_VERSION = os.environ["API_VERSION"]
AZURE_DEPLOYMENT = os.environ["AZURE_DEPLOYMENT"]
OPENAI_API_TYPE = os.environ["OPENAI_API_TYPE"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

def parse_args(args):
    parser = argparse.ArgumentParser("Prompt file")
    parser.add_argument("-cy", "--cypher", help="txt Cypher Prompt File", required=True)
    parser.add_argument("-qal", "--loanPrompt", help="txt Agent Prompt File for Loans", required=True)
    parser.add_argument("-qam", "--metadataPrompt", help="txt Agent Prompt File for Metadata", required=True)

    return parser.parse_args(args)

args = parse_args(sys.argv[1:])

def read_prompt_file(filename):
    """
    Reads the contents of the prompt file.
    """
    with open(filename, "r") as f:
        return f.read()

cypher_prompt_text = read_prompt_file(args.cypher)

loan_prompt = read_prompt_file(args.loanPrompt)
metadata_prompt = read_prompt_file(args.metadataPrompt)


def get_system_message(schema) -> str:
    system_message = cypher_prompt_text
    system_message += f"""
    Schema: 
    {schema}
    """
    return system_message

def get_examples_message(examples) -> str:
    if examples:
        return f"""
        Below are some examples to guide your transformation. Use this as a reference to generate the Cypher query:
        {examples}
        """
    else:
        return "No similar examples found in the database"

# Helper function to write messages
def write_message(role, content, save=True):
    """
    Saves a message to session state and writes it to the UI
    """
    # Append to session state
    if save:
        if "messages" not in st.session_state:
            st.session_state.messages = []
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)

# Session ID Access
def get_session_id():
    return st.session_state.session_id
