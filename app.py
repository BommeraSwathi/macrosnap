import streamlit as st
from google import genai
from prompts import SYSTEM_PROMPT

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🥗 MacroSnap")
st.write("Snap your meal and get an estimated calorie & macro breakdown.")

uploaded_file = st.file_uploader(
    "Upload a photo of your meal",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Your meal", use_container_width=True)

    if st.button("Analyze Meal"):
        with st.spinner("Analyzing your meal..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    SYSTEM_PROMPT,
                    {
                        "inline_data": {
                            "mime_type": uploaded_file.type,
                            "data": uploaded_file.getvalue()
                        }
                    }
                ]
            )

            st.subheader("🍽️ Result")
            st.write(response.text)