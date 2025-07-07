import streamlit as st
import requests

st.title("💡 AI Content Generator")
st.caption("Generate content using Amazon Bedrock")

prompt = st.text_input("Enter keywords or description:")

if st.button("Generate"):
    if not prompt:
        st.warning("Please enter some keywords or a description.")
    else:
        try:
            response = requests.post(
                "https://fcfvcce3v3.execute-api.us-east-1.amazonaws.com/generate",
                json={"keywords": prompt}
            )
            if response.status_code == 200:
                data = response.json()
                st.success("Generated Content:")
                st.write(data.get("generated_content", "No content found."))
            else:
                st.error(f"Failed to generate content: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")

# Optional: Show history
if st.button("Show History"):
    try:
        response = requests.get("https://fcfvcce3v3.execute-api.us-east-1.amazonaws.com/history")
        if response.status_code == 200:
            history = response.json().get("history", [])
            st.subheader("Previous Prompts")
            for item in history:
                st.markdown(f"• {item.get('keywords')} ➜ {item.get('content')}")
        else:
            st.error("Failed to fetch history.")
    except Exception as e:
        st.error(f"Error: {e}")