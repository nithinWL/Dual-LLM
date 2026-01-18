import streamlit as st
import requests
import json


st.set_page_config(
    page_title="Dual-LLM Q&A Generator",
    page_icon="🤖",
    layout="centered",
)


st.title("🤖 Dual-LLM Q&A Session Generator")
st.markdown(
    """
Generate a multi-turn **question–answer session** using two LLM-based agents.
- Difficulty increases gradually
- Previous Q/A pairs are used as context
- Output can be downloaded as JSON
"""
)

st.divider()


with st.form("qa_form"):
    subject = st.text_input(
        "Subject",
        placeholder="e.g. Computer Networks, Quantum Mechanics, Linear Algebra"
    )

    num_pairs = st.number_input(
        "Number of Q&A pairs",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

    submit = st.form_submit_button("🚀 Run Session")


if submit:
    if not subject.strip():
        st.error("Please enter a valid subject.")
    else:
        with st.spinner("Generating Q&A session..."):
            try:
                response = requests.post(
                    "http://localhost:8000/run-session",
                    json={
                        "subject": subject,
                        "num_pairs": num_pairs
                    },
                    timeout=120,
                )

                if response.status_code != 200:
                    st.error(f"API Error: {response.text}")
                else:
                    data = response.json()
                    st.success("Q&A session generated successfully!")

                    st.divider()

                    for pair in data["pairs"]:
                        st.markdown(f"### Q{pair['id']}: {pair['question']}")

                        with st.expander("Show Answer"):
                            # Markdown renders LaTeX equations correctly
                            st.markdown(pair["answer"])

                    st.divider()

                    st.download_button(
                        label="⬇️ Download Q&A as JSON",
                        data=json.dumps(data, indent=2),
                        file_name="qa_session.json",
                        mime="application/json"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")
