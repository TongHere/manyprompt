import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def translate_sentence(sentence, gender, casual_level):
    messages = [
        {"role": "system", "content": f"You are an expert linguist, specializing in the structure, meaning, usage, and evolution of language. With advanced education in linguistics, you possess multilingual proficiency, exceptional analytical and critical thinking skills, cultural sensitivity, and strong communication abilities. Your expertise includes conducting in-depth linguistic research, problem-solving, and effectively using technological tools to analyze linguistic phenomena. Provide thoughtful, detailed, and precise responses, demonstrating linguistic clarity, insight, and cultural awareness in your explanations. Translate the sentence from English to German and considering the speaker's gender as {gender}. The tone should be {casual_level}."},
        {"role": "user", "content": sentence}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def main():
    st.title(" Your Translator BFF")

    if 'translation' not in st.session_state:
        st.session_state.translation = ""
    if 'step' not in st.session_state:
        st.session_state.step = 'input'

    # Step 1: User enters the sentence to translate
    if st.session_state.step == 'input':
        sentence = st.text_input("Enter the sentence you want to translate:")
        if sentence:
            st.session_state.sentence = sentence
            st.session_state.step = 'gender'

    # Step 2: Ask for gender preference
    if st.session_state.step == 'gender':
        st.subheader("Speaker Gender")
        
        # Initialize chat history if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [{"role": "assistant", "content": "Is the speaker male or female?"}]
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "assistant":
                st.markdown(f"**Assistant:** {message['content']}")
            else:
                st.markdown(f"**You:** {message['content']}")
        
        # Add a text input for interaction
        user_response = st.text_input("Your response:", key="gender_response", placeholder="Type 'male' or 'female'...")
        
        # Process the response when user submits
        if user_response.lower() in ['male', 'female']:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_response})
            
            # Store the gender and move to next step
            st.session_state.gender = user_response.capitalize()
            st.session_state.step = 'translate'
            st.experimental_rerun()
        elif user_response and user_response.lower() not in ['male', 'female']:
            st.error("Please type either 'male' or 'female'.")

    # Step 3: Perform initial translation (default neutral)
    if st.session_state.step == 'translate':
        translation = translate_sentence(
            st.session_state.sentence, st.session_state.gender, "neutral"
        )
        st.session_state.translation = translation
        st.markdown(f"**Translation:** {translation}")
        st.session_state.step = 'casual'

    # Step 4: Ask continuously if user wants more casual translation
    if st.session_state.step == 'casual':
        # Display the current translation
        st.markdown(f"**Translation:** {st.session_state.translation}")
        
        # Display chat-like message from the system
        st.write("**Assistant:** Do you want to make the translation more casual?")
        
        # Create a container for user input
        casual_input_container = st.container()
        
        # Add a text input for chat-style interaction
        with casual_input_container:
            casual_response = st.text_input("Your response:", key="casual_response", 
                                           placeholder="Type 'yes' or 'no'...")
            
            # Process the response when user submits
            if casual_response.lower() in ['yes', 'y']:
                # Display user's message in chat style
                st.write(f"**You:** {casual_response}")
                
                # Generate more casual translation
                translation = translate_sentence(
                    st.session_state.sentence, st.session_state.gender, "more casual"
                )
                st.session_state.translation = translation
                st.markdown(f"**Casual Translation:** {translation}")
                
                # Ask if user wants to translate another sentence
                st.write("**Assistant:** Would you like to translate another sentence?")
                another_response = st.text_input("Your response:", key="another_response", 
                                               placeholder="Type 'yes' or 'no'...")
                
                if another_response.lower() in ['yes', 'y']:
                    st.session_state.clear()
                    st.experimental_rerun()
                    
            elif casual_response.lower() in ['no', 'n']:
                # Display user's message in chat style
                st.write(f"**You:** {casual_response}")
                
                # Display final translation
                st.markdown(f"**Final Translation:** {st.session_state.translation}")
                
                # Ask if user wants to translate another sentence
                st.write("**Assistant:** Would you like to translate another sentence?")
                another_response = st.text_input("Your response:", key="another_response", 
                                               placeholder="Type 'yes' or 'no'...")
                
                if another_response.lower() in ['yes', 'y']:
                    st.session_state.clear()
                    st.experimental_rerun()
                    
            elif casual_response and casual_response.lower() not in ['yes', 'y', 'no', 'n']:
                st.error("Please type either 'yes' or 'no'.")

if __name__ == '__main__':
    main()
