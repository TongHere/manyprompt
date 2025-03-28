import streamlit as st
import os
import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Load prompts from YAML file - do this once at startup
@st.cache_resource
def load_prompts():
    with open('prompts.yaml', 'r') as file:
        return yaml.safe_load(file)

prompts = load_prompts()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def translate_sentence(sentence, gender, casual_level):
    try:
        messages = [
            {"role": "system", "content": prompts['translator']['system'].format(gender=gender, casual_level=casual_level)},
            {"role": "user", "content": sentence}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None
def main():
    st.title(prompts['ui']['title'])

    if 'translation' not in st.session_state:
        st.session_state.translation = ""
    if 'step' not in st.session_state:
        st.session_state.step = 'input'

    # Step 1: User enters the sentence to translate
    if st.session_state.step == 'input':
        sentence = st.text_input(prompts['ui']['input_prompt'])
        if sentence:
            st.session_state.sentence = sentence
            st.session_state.step = 'gender'

    # Step 2: Ask for gender preference
    if st.session_state.step == 'gender':
        st.subheader(prompts['labels']['gender_subheader'])
        
        # Display the question
        st.write(prompts['ui']['gender_question'])
        
        # Add a text input for interaction
        user_response = st.text_input("Your response:", key="gender_response", 
                                     placeholder=prompts['ui']['gender_placeholder'])
        
        # Process the response when user submits
        if user_response.lower() in ['male', 'female']:
            # Display confirmation
            st.write(f"**You:** {user_response}")
            
            # Store the gender and move to next step
            st.session_state.gender = user_response.capitalize()
            st.session_state.step = 'translate'
            st.experimental_rerun()
        elif user_response and user_response.lower() not in ['male', 'female']:
            st.error(prompts['ui']['gender_error'])

    # Step 3: Perform initial translation (default neutral)
    if st.session_state.step == 'translate':
        translation = translate_sentence(
            st.session_state.sentence, st.session_state.gender, "neutral"
        )
        st.session_state.translation = translation
        st.markdown(f"**{prompts['labels']['translation']}** {translation}")
        st.session_state.step = 'casual'

    # Step 4: Ask continuously if user wants more casual translation
    if st.session_state.step == 'casual':
        # Display the current translation
        st.markdown(f"**{prompts['labels']['translation']}** {st.session_state.translation}")
        
        # Display chat-like message from the system
        st.write(f"**Assistant:** {prompts['ui']['casual_question']}")
        
        # Create a container for user input
        casual_response = st.text_input("Your response:", key="casual_response", 
                                       placeholder=prompts['ui']['casual_placeholder'])
        
        # Process the response when user submits
        if casual_response.lower() in ['yes', 'y']:
            # Display user's message in chat style
            st.write(f"**You:** {casual_response}")
            
            # Generate more casual translation
            translation = translate_sentence(
                st.session_state.sentence, st.session_state.gender, "more casual"
            )
            st.session_state.translation = translation
            st.markdown(f"**{prompts['labels']['casual_translation']}** {translation}")
            
            # Ask if user wants to translate another sentence
            st.write(f"**Assistant:** {prompts['ui']['another_question']}")
            another_response = st.text_input("Your response:", key="another_response", 
                                           placeholder=prompts['ui']['another_placeholder'])
            
            if another_response.lower() in ['yes', 'y']:
                st.session_state.clear()
                st.experimental_rerun()
                
        elif casual_response.lower() in ['no', 'n']:
            # Display user's message in chat style
            st.write(f"**You:** {casual_response}")
            
            # Display final translation
            st.markdown(f"**{prompts['labels']['final_translation']}** {st.session_state.translation}")
            
            # Ask if user wants to translate another sentence
            st.write(f"**Assistant:** {prompts['ui']['another_question']}")
            another_response = st.text_input("Your response:", key="another_response", 
                                           placeholder=prompts['ui']['another_placeholder'])
            
            if another_response.lower() in ['yes', 'y']:
                st.session_state.clear()
                st.experimental_rerun()
                
        elif casual_response and casual_response.lower() not in ['yes', 'y', 'no', 'n']:
            st.error(prompts['ui']['casual_error'])

if __name__ == '__main__':
    # Add this before processing the sentence
    if not sentence or sentence.isspace():
        st.error("Please enter a valid sentence to translate.")
        return

    def get_user_response(prompt, placeholder, error_message, valid_responses):
        st.write(f"**Assistant:** {prompt}")
        user_response = st.text_input("Your response:", key=f"response_{prompt[:10]}", 
                                     placeholder=placeholder)
        
        if user_response.lower() in valid_responses:
            st.write(f"**You:** {user_response}")
            return user_response.lower()
        elif user_response and user_response.lower() not in valid_responses:
            st.error(error_message)
            return None
        return None

    main()