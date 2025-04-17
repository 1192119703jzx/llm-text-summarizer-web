import streamlit as st

def summarization_page(cookie_manager):
    cookie_manager.set("current_page", "summarization", key="set_current_page")

    st.title("Text Summarization")
    st.markdown("### Enter the text or upload the file you want to summarize")

    # Text input for user to enter text
    text_input = st.text_area("Enter your text here", height=200)

    st.markdown("---")
    if st.button("Back to home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()