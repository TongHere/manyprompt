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
        st.subheader(" Audience Gender")
        
        # Display chat-like message from the system
        with st.chat_message("assistant"):
            st.write("Is the speaker male or female?")
        
        # Create a container for user input
        user_input_container = st.container()
        
        # Add a text input for chat-style interaction
        with user_input_container:
            user_response = st.text_input("Your response:", key="gender_response", placeholder="Type 'male' or 'female'...")
            
            # Process the response when user submits
            if user_response.lower() in ['male', 'female']:
                # Display user's message in chat style
                with st.chat_message("user"):
                    st.write(user_response)
                
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
        more_casual = st.radio(
            "Do you want to make the translation more casual?", ('Yes', 'No')
        )
        if more_casual == 'Yes':
            translation = translate_sentence(
                st.session_state.sentence, st.session_state.gender, "more casual"
            )
            st.session_state.translation = translation
            st.markdown(f"**Casual Translation:** {translation}")
        else:
            st.markdown(f"**Final Translation:** {st.session_state.translation}")
            if st.button("Translate Another Sentence"):
                st.session_state.clear()
                st.experimental_rerun()

if __name__ == '__main__':
    main()
