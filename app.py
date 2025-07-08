sneha-feature
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

import streamlit as st
import requests

API_BASE_URL = "https://fcfvcce3v3.execute-api.us-east-1.amazonaws.com"

st.set_page_config(page_title="💡 AI Content Generator", layout="centered")

st.title("💡 AI Content Generator")
st.write("Generate creative content using Amazon Bedrock")

# --- Main input to generate content ---
keywords = st.text_input("Enter keywords or short description:")

if st.button("Generate"):
    if not keywords.strip():
        st.error("Please enter keywords or description to generate content.")
    else:
        with st.spinner("Generating content..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate",
                    json={"keywords": keywords},
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                if response.status_code == 200:
                    data = response.json()
                    content = data.get("generated_content", "")
                    st.success("Generated content:")
                    st.write(content)
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

# --- Sidebar history (LIFO: Last In First Out) ---
st.sidebar.header("🕘 Search History")

history_lookup = {}
selected_keyword = None

try:
    history_response = requests.get(f"{API_BASE_URL}/history", timeout=10)
    if history_response.status_code == 200:
        history_data = history_response.json()
        raw_history = history_data.get("history", [])  # do NOT reverse here

        # We’ll build a reversed unique list (LIFO)
        seen = set()
        unique_lifo = []
        for item in reversed(raw_history):  # reversed here so latest is first
            keyword = item.get("keywords", "").strip()
            if keyword and keyword not in seen:
                seen.add(keyword)
                unique_lifo.append(keyword)
                history_lookup[keyword] = item.get("content", "")

        if unique_lifo:
            selected_keyword = st.sidebar.radio("Select a keyword:", unique_lifo, index=None)
        else:
            st.sidebar.info("No search history yet.")
    else:
        st.sidebar.error("Failed to load history.")
except Exception as e:
    st.sidebar.error(f"Error: {e}")

# --- Show content only when clicked ---
if selected_keyword:
    st.markdown("---")
    st.subheader(f"📌 Content for: *{selected_keyword}*")
    st.write(history_lookup[selected_keyword])
    main
