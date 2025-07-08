import streamlit as st
import requests

# Streamlit page setup with sidebar expanded
st.set_page_config(
    page_title="💡 AI Content Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("💡 AI Content Generator")
st.caption("Generate content using Amazon Bedrock")

# Session state to store prompt history
if 'history' not in st.session_state:
    st.session_state.history = []

# Input field
prompt = st.text_input("Enter keywords or description:")

# API Gateway URL (use your real endpoint)
API_URL = "https://fcfvcce3v3.execute-api.us-east-1.amazonaws.com"

# Generate button logic
if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter a valid prompt.")
    else:
        try:
            response = requests.post(API_URL, json={"prompt": prompt})
            response_json = response.json()

            if response.status_code == 200:
                generated = response_json.get("generated_content", "⚠️ No content returned.")
                st.success("✅ Content generated successfully!")
                st.write(generated)

                # Save to history
                st.session_state.history.append({
                    "keywords": prompt,
                    "content": generated
                })

            else:
                st.error(f"❌ Error: {response_json.get('error', 'Unknown error occurred.')}")
        except Exception as e:
            st.error(f"⚠️ Exception: {str(e)}")

# Sidebar History Panel
with st.sidebar:
    st.header("📜 Prompt History")

    if st.session_state.history:
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"**• {item['keywords']}**\n> {item['content'][:80]}...")
    else:
        st.info("No history yet. Generate some prompts!")