import streamlit as st
from utils import write_message
from agent import agent

# Page configuration
ICON_PATH = 'logo.png'
ICON = 'assets/icon.png'
st.set_page_config("Knowledge Graph Q&A Sidekick", page_icon=ICON, layout="wide")

# FAQs for each selection
FAQS = {
    "Loss Draft Loan Q&A": [
        "What is the loan servicing status for the loan linked to client number 978?",
        "What is the current tracking status of the loan 8209527981?",
        "Which loans will mature within the next 6 months?",
        "What loans have escrow balances above $3700 and what are their loan types?",
        "Which loans have escrow balances above $3,000 and are classified as 'Non Escrow'?"
    ],
    "Report Metadata Q&A": [
        "What are the reports that contain the term 'Borrower'?",
        "In which tables I can find the term 'UPB'",
        "Show me opportunities to consolidate reports in the funitonal area Loss Draft",
        " What is definition of 'Client Name'?",
        "What is the definition for Active Flag?"
    ]
}

# Custom CSS for styling
st.markdown(
    """
    <style>
        .header {
            text-align: center;
            margin-bottom: 0px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header h2 {
            color: #6c757d;
            font-size: 1.2em;
            margin-bottom: 20px;
        }
        .faq-container {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            margin: 20px auto;
            width: 60%;
        }
        .faq-container h3 {
            color: #007bff;
        }
        .chat-container {
            margin: 20px auto;
            width: 60%;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state initialization
if 'data_selection' not in st.session_state:
    st.session_state.data_selection = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Main App Page
st.image(ICON_PATH, width=250)
st.markdown(
    """
    <div class="header">
        <h1>Knowledge Graph Q&A Sidekick</h1>
        <h2>The Knowledge Graph Q&A Sidekick helps you gain insights into Reporting Metadata using Neo4J Graph Database — powered by GenAI.</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.data_selection is None:
    st.markdown("### <span style='font-size:18px;'>Please choose one of the options:</span>", unsafe_allow_html=True)
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    loan_clicked = st.button("Loss Draft Loan Q&A", key="loan")
    metadata_clicked = st.button("Report Metadata Q&A", key="metadata")
    st.markdown('</div>', unsafe_allow_html=True)

    if loan_clicked:
        st.session_state.data_selection = "Loss Draft Loan Q&A"
        agent.select_prompt_from_selection()
        st.rerun()
    elif metadata_clicked:
        st.session_state.data_selection = "Report Metadata Q&A"
        agent.select_prompt_from_selection()
        st.rerun()
else:
    st.markdown(f"<div class='selected-text'>You selected: <strong>{st.session_state.data_selection}</strong></div>", unsafe_allow_html=True)
    
    # Display FAQ Section
    st.markdown("<div class='faq-container'>", unsafe_allow_html=True)
    st.markdown(f"<h5>Frequently Asked Questions</h5>", unsafe_allow_html=True)
    for question in FAQS[st.session_state.data_selection]:
        st.markdown(f"- {question}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Knowledge Graph Q&A Sidekick! How can I help you?"}]

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        write_message(message['role'], message['content'], save=False)
    st.markdown('</div>', unsafe_allow_html=True)

    def handle_submit(message):
        with st.spinner('Thinking...'):
            response = agent.generate_response(message)
            write_message('assistant', response)

    if question := st.chat_input("Ask a question..."):
        write_message('user', question)
        handle_submit(question)

    if len(st.session_state.messages) > 1:
        if st.button("Reset", key="reset"):
            st.session_state.data_selection = None
            st.session_state.messages = []
            st.rerun()
