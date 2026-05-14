# GraphIQ Assistant – Q&A with Neo4j + LLM

An enterprise-grade graph-based question answering assistant that converts natural language queries into Cypher queries and retrieves structured insights from Neo4j using Large Language Models (LLMs).



## Overview

GraphIQ Assistant enables users to interact with enterprise metadata and graph data using plain English.

The system:

- Understands user queries using GPT-4
- Dynamically generates Cypher queries
- Executes queries on Neo4j
- Retrieves context-aware graph-based responses
- Supports intelligent metadata exploration

This project was designed to simplify enterprise data discovery and improve accessibility to graph-based knowledge systems.



## Key Features

- Natural Language → Cypher Query Generation
- Neo4j Graph Database Integration
- Azure OpenAI GPT-4 Integration
- Context-Aware Enterprise Metadata Search
- Prompt Engineering for Graph Query Optimization
- Dynamic Query Generation using LangChain
- Semantic Graph-Based Knowledge Retrieval
- Modular Agent-Based Architecture
- Enterprise AI Chatbot Workflow



## Tech Stack

- Python
- Neo4j
- Azure OpenAI
- GPT-4
- LangChain
- Streamlit
- Prompt Engineering
- Docker
- Azure Web Apps



## Architecture


```text
User Query
    ↓
LLM Agent
    ↓
Cypher Query Generation
    ↓
Neo4j Graph Database
    ↓
Response Generation
```




## Project Structure


prompts/               Prompt templates
assets/                Static assets
app.py                 Main application
agent.py               Agent orchestration
llm.py                 Azure OpenAI integration
neo4j_gpt_query.py     Graph querying logic
example_provider.py    Semantic example retrieval
metadata_examples.py   Metadata query examples
utils.py               Utility functions
run.sh                 Application startup script




## Example Queries

- Which reports are related to the term **"Client Id"**?
- Show all reports under **Loss Draft** domain.
- Which tables contain the term **"Inspection"**?
- Find metadata related to **Service Level**.
- What reports can be consolidated in a functional area?






## Screenshots

### Chat Interface
<img width="1917" height="988" alt="Screenshot 2026-05-14 161928" src="https://github.com/user-attachments/assets/bbfe74d7-8f70-4995-921f-45bdc8e40f1b" />

### Cypher Query Generation

<img width="1540" height="1048" alt="image" src="https://github.com/user-attachments/assets/70f46626-52a9-4310-9a31-2a130f7929cf" />
<img width="1525" height="1041" alt="image" src="https://github.com/user-attachments/assets/979d65d5-b89f-4d92-a5ea-b47a9d8eee9e" />

### Output 

<img width="1918" height="827" alt="image" src="https://github.com/user-attachments/assets/ac9946bd-39b4-4266-9e2b-9eb9af643ea5" />
<img width="1918" height="941" alt="image" src="https://github.com/user-attachments/assets/b3220919-8e68-47d9-b67e-ce534d0d50ce" />

### Neo4j Graph 

<img width="1918" height="962" alt="image" src="https://github.com/user-attachments/assets/4cff9f9c-37d0-4b7b-85d1-b604dd8a95b9" />

### Azure Deployment

<img width="1780" height="818" alt="image" src="https://github.com/user-attachments/assets/3938af62-4f36-441b-8f84-34b42bd5f28e" />
<img width="1667" height="823" alt="image" src="https://github.com/user-attachments/assets/36f65b49-c830-40f5-8c32-31572534d4ab" />


## Deployment

The application was deployed internally on enterprise Azure infrastructure using:

- Azure Web Apps
- Azure OpenAI Services
- Neo4j Graph Database

---

## Learning Outcomes

This project strengthened expertise in:

- LLM-powered application development
- Knowledge Graph engineering
- Prompt Engineering
- Neo4j graph modeling
- LangChain orchestration
- Azure AI ecosystem
- Enterprise AI deployment workflows



## Security Note

This repository contains a sanitized version of the project.  
Production credentials, internal endpoints, and enterprise configurations have been removed.


## Business Impact

- Reduced metadata discovery time by ~74%
- Enabled natural language access to enterprise knowledge graphs
- Improved accessibility of technical metadata for non-technical users



## Author

**Shivansh Bhatia**
































