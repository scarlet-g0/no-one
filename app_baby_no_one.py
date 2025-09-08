import streamlit as st
import uuid
from baby_no_one import BabyNoOne, run_baby_no_one, langfuse_client

# Configure page
st.set_page_config(
    page_title="Baby-NO.ONE Chat",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for minimal styling
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stChatMessage {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 1px solid #ddd;
        padding: 10px 15px;
    }
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        min-height: 400px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agent' not in st.session_state:
    st.session_state.agent = BabyNoOne(provider='google', langfuse_client=langfuse_client)

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input field at the bottom
user_input = st.chat_input("Ask a question...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Show thinking status
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.write("Thinking...")
        
        try:
            # Get agent response
            response = run_baby_no_one(
                st.session_state.agent, 
                user_input, 
                st.session_state.session_id
            )
            
            # Replace thinking message with actual response
            thinking_placeholder.empty()
            st.write(response)
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            thinking_placeholder.empty()
            error_msg = f"Error: {str(e)}"
            st.write(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Rerun to update the display
    st.rerun()