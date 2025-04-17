import streamlit as st
from db_instance import db
from user import logout
import time

def home_page(cookie_manager):
    cookie_manager.set("current_page", "home", key="set_current_page")

    # Sidebar
    with st.sidebar:
        st.subheader(f"👤 {st.session_state.username}")
        st.markdown("---")
        
        '''
        # User preferences
        if st.button("View or Edit My Preferences📝", use_container_width=True):
            st.session_state.page = "preferences"
        '''

        st.markdown("---")
        # Logout button
        if st.button("Logout", use_container_width=True):
            logout(cookie_manager)

        '''
        st.subheader("History 📖")
        history_list = db.get_user_history(st.session_state.id)
        items_per_page = 5
        total_pages = (len(history_list) + items_per_page - 1) // items_per_page

        if "history_page" not in st.session_state:
            st.session_state.history_page = 1

        # Display history items for the current page
        start_idx = (st.session_state.history_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_page_items = history_list[start_idx:end_idx]

        for i, item in enumerate(current_page_items):
            if st.sidebar.button(item, key=f"content_match_{i}"):
                # some how redirect to the corresponding summarization page
                pass

        # Pagination controls
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️", disabled=st.session_state.history_page <= 1):
                st.session_state.history_page -= 1
        with col3:
            if st.button("➡️", disabled=st.session_state.history_page >= total_pages):
                st.session_state.history_page += 1
        with col2:
            st.write(f"{st.session_state.history_page} / {total_pages}")
        '''


    # Main page layout
    st.title(f"Welcome back, {st.session_state.username}! 👋")
    st.markdown("### LLM-Based Text Summarization")

    # Creative elements
    if st.button("✨ Start New Summarization", use_container_width=True):
        st.session_state.page = "first_preference"
        st.rerun()
        
    st.markdown("---")

    # search bar
    st.subheader("Search summarization from your history 🔍")
    search_term = st.text_input("", placeholder="enter the key word you want to search")
    pass

