import streamlit as st
import requests

from connections import GROQ_ENDPOINT, MODEL, USE_LOCAL, build_prompt, headers
from pricing_data import pricing_data

st.set_page_config(page_title="Goodknight Vet Assistant", layout="centered")
st.title("🐾 Goodknight Mobile Vet Assistant")

# Keep chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Ask a question about pricing, services, or pet care:")

# Handle submission
if user_input:
    with st.spinner("Thinking..."):
        if USE_LOCAL:
            payload = {
                "prompt": build_prompt(user_input, pricing_data),
                "temperature": 0.3,
                "max_tokens": 512
            }
        else:
            payload = {
                "model": MODEL,
                    "messages": [
                        {"role": "system", "content": "You are a helpful veterinary assistant."},
                        {"role": "user", "content": build_prompt(user_input, pricing_data)}
                    ],
                "temperature": 0.3
            }

        try:
            response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"FATAL Error: {e}")
            quit()

        reply = response.json()
        text = (
            reply.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "Hmm, I didn't get that.")
        )

        # Save to history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("VetBot", text))

# Display chat history
for speaker, msg in reversed(st.session_state.chat_history):
    st.markdown(f"**{speaker}:** {msg}")
