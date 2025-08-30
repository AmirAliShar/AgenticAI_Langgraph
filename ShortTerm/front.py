import streamlit as st
import requests
import time

# Configuration
API_URL = "http://localhost:8000/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 AI Chatbot")
st.markdown("Chat with an AI assistant using your FastAPI endpoint")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Simulate typing effect
            message_placeholder.markdown("▌")
            
            # Call your FastAPI endpoint
            response = requests.post(
                API_URL,
                json={"message": prompt},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                full_response = data["response"]
                
                # Display with typing effect
                for chunk in full_response.split():
                    full_response_chunk = chunk + " "
                    message_placeholder.markdown(full_response_chunk + "▌")
                    time.sleep(0.05)
                    full_response_chunk += chunk + " "
                
                message_placeholder.markdown(full_response)
                
            else:
                error_msg = f"API Error: {response.status_code}"
                message_placeholder.markdown(error_msg)
                
        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to the API. Is the server running?"
            message_placeholder.markdown(error_msg)
            
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            message_placeholder.markdown(error_msg)
    
    # Add assistant response to history
    if full_response:
      
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar info
with st.sidebar:
     st.header("Settings")
     st.info("This chatbot connects to your FastAPI LangGraph endpoint")
     st.code("""
    # To run your API:
    # uvicorn main:app --reload --port 8000
    """)