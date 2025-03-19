import json
import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def main():
    st.title("Chat with LLM")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**User:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")
    
    # Replace chat_input with text_input
    prompt = st.text_input("What would you like to ask?")
    
    if prompt:
        if 'last_prompt' not in st.session_state or st.session_state.last_prompt != prompt:
            st.session_state.last_prompt = prompt
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            st.markdown(f"**User:** {prompt}")
            
            # Get clarifying question
            clarifying_question = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ask the user if they prefer a male or female tone, and if they prefer a casual, funny, or formal response."},
                    {"role": "user", "content": prompt}
                ]
            ).choices[0].message.content
            
            st.markdown(f"**Assistant:** {clarifying_question}")
            st.session_state.messages.append({"role": "assistant", "content": clarifying_question})
            
            # Get user clarification
            user_clarification = st.text_input("Please specify your preference:")
            
            if user_clarification:
                final_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"Respond with a {user_clarification} tone."},
                        {"role": "user", "content": prompt}
                    ]
                ).choices[0].message.content
                
                st.markdown(f"**Assistant:** {final_response}")
                st.session_state.messages.append({"role": "assistant", "content": final_response})

if __name__ == '__main__':
    main()