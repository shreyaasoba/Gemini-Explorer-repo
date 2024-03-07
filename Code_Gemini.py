import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "gemini-explorer-415718"

vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4,
    top_p=0.6
)

model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)

chat = model.start_chat()


# Helper function
def llm_function(chat: ChatSession, query, user_name):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    # Personalize ReX's response with the user's name
    personalized_output = f"{output}, {user_name}!"

    with st.chat_message("model"):
        st.markdown(personalized_output)

    # Use session_state for persistent chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": personalized_output
        }
    )


# Initialize the chat history (outside the conditional block)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Capture the user's name
user_name = st.text_input("Please enter your name")

# Display and load chat history using a loop
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role=message["role"],
        parts=[Part.from_text(message["content"])]
    )
    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content)


# For initial message startup
initial_prompt = f"Hello {user_name}, I'm ReX, an assistant powered by Google Gemini. Use emojis to be interactive."
llm_function(chat, initial_prompt, user_name)

# For capturing user input
query = st.chat_input("Gemini Explorer - Please give your name")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query, user_name)