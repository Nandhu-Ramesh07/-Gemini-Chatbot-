import google.generativeai as genai
import streamlit as st

genai.configure(api_key="xxxx-xxx-xxxx-xxxx-xxxxxxx")

model = genai.GenerativeModel("gemini-1.5-flash")

def get_response(context, user_message):
    # Combine the history into a single context string
    full_context = "\n".join([f"User: {c['user']}\nAI: {c['bot']}" for c in context]) 
    prompt = f"{full_context}\nUser: {user_message}\nAI:"
    
    # Generate response
    response = model.generate_content(prompt, stream=True)
    result = ""
    for chunk in response:
        result += chunk.text
    return result

# Streamlit app configuration
st.set_page_config(page_title="Hello.ai", layout="centered")

# App Title
st.title("Hello.ai")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

with st.sidebar:
    st.header("Conversation History")
    if st.session_state.conversation:
        for i, exchange in enumerate(st.session_state.conversation, 1):
            st.write(f"**{i}. You:** {exchange['user']}")
            st.write(f"**{i}. Hello.ai:** {exchange['bot']}")
    else:
        st.write("No conversation history yet.")

# Input field for user message
user_input = st.text_input("Enter your message:")

# "Get Response" Button
if st.button("Get Response") or st.session_state.get("user_input"):
    if user_input:
        # Generate the response
        bot_response = get_response(st.session_state.conversation, user_input)

        # Update conversation history
        st.session_state.conversation.append({"user": user_input, "bot": bot_response})

if st.session_state.conversation:
    latest_exchange = st.session_state.conversation[-1]
    st.markdown(
        f"<p style='color:blue;'><b>Hello.ai:</b> {latest_exchange['bot']}</p>",
        unsafe_allow_html=True,
    )
else:
    st.write("Start chatting to see responses here!")