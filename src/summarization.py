import streamlit as st
from db_instance import db
import time
from deepseek_api import chat_api


def summarize_text(text, preference):
    max_tokens = preference["max_tokens"]
    temperature = preference["temperature"]
    style = preference["style"]
    model = 'deepseek-chat'
    response = chat_api(model=model, max_tokens=max_tokens, text=text, temperature=temperature, style=style)
    return response[0] if response else "Error: No response from API"


def summarization_page(cookie_manager):
    cookie_manager.set("current_page", "summarization", key="set_current_page")

    st.title("Text Summarization")
    st.markdown("### Enter the text or upload the file you want to summarize")

    # Text input for user to enter text
    text_input = st.text_area("", height=200)

    # file upload
    MAX_FILE_SIZE = 10 * 1024 * 1024
    uploaded_file = st.file_uploader("Choose a file to summarize", type=["txt"], help="Max file size: 10MB")
    if uploaded_file is not None:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"File too large! Max size is 10 MB")
        else:
            text_input = uploaded_file.read().decode("utf-8")
    
    # submit button
    if st.button("Submit", use_container_width=True):
        st.success("Submit successfully, working on it...")
        if text_input:
            summary = summarize_text(text_input, st.session_state.using_preference)  # Placeholder for actual summarization function
            st.markdown("### Summary:")
            with st.expander("View Summary"):
                st.write(summary)

            # store the summary in user history
            summary_name = summary[:20] + "..." if len(summary) > 20 else summary
            summary_id = db.add_summarization_history(st.session_state.id, text_input, summary, summary_name)
            if st.session_state.user_history:
                st.session_state.user_history.append((summary_id, summary_name))
            else:
                st.session_state.user_history = [(summary_id, summary_name)]
        else:
            st.warning("Please enter text or upload a file to summarize.")

    st.markdown("---")
    if st.button("Back to home", use_container_width=True):
        st.session_state.using_preference = None
        st.session_state.page = "home"
        st.rerun()


def history_summary_page(cookie_manager, document_tuple):
    cookie_manager.set("current_page", "history_summary", key="set_current_page")
    document_id = document_tuple[0]
    document = db.get_document_by_id(document_id)
    if not document:
        st.error("Document not found.")
        return
    
    # Display the document
    st.title(document['name'])
    with st.expander("View Document"):
        st.write(document['text'])
    st.markdown(f"### Day of summarization: {document['date']}")
    st.markdown("---")
    with st.expander("Summary"):
        st.write(document['summary'])

    if st.button("Delete this summary", use_container_width=True):
        db.delete_document_by_id(document_id)
        st.session_state.user_history.remove(document_tuple)
        st.success("Summary deleted successfully!")
        time.sleep(1)
        st.session_state.target_history = None
        st.session_state.page = "home"
        st.rerun()

    if st.button("Back to home", use_container_width=True):
        st.session_state.target_history = None
        st.session_state.page = "home"
        st.rerun()
