from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv() 

# Create the LLM
llm = AzureChatOpenAI(
    azure_endpoint= "https://aidatascience.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview",
    openai_api_version= os.environ["API_VERSION"],
    openai_api_type= os.environ["OPENAI_API_TYPE"],
    openai_api_key= os.environ["OPENAI_API_KEY"],
    azure_deployment= "gpt-4o",
    temperature=0,
)

# Create the Embedding model

embeddings_provider = AzureOpenAIEmbeddings(
    openai_api_key= os.environ["OPENAI_API_KEY"],
    azure_endpoint= os.environ["AZURE_ENDPOINT"]
)
