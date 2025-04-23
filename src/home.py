import streamlit as st
from db_instance import db
from user import logout
import time
import json

def home_page(cookie_manager):
    cookie_manager.set("current_page", "home", key="set_current_page")

    # Sidebar
    with st.sidebar:
        st.subheader(f"👤 {st.session_state.username}")
        st.markdown("---")
        
        # User preferences
        if st.button("Delete saved Preferences📝", use_container_width=True):
            st.session_state.page = "delete_preferences"
            st.rerun()

        st.markdown("---")
        # Logout button
        if st.button("Logout", use_container_width=True):
            logout(cookie_manager)

        if st.button("Delete your account", use_container_width=True):
            db.delete_user(st.session_state.id)
            logout(cookie_manager)

        # Present user history
        # Potential implmentration sort by data, (Today, in 7Days, in 30Days)
        st.markdown("---")

        st.subheader("History 📖")

        if "history_page" not in st.session_state:
            st.session_state.history_page = 1

        items_per_page = 5
        total_pages = 0

        if st.session_state.user_history:
            total_pages = (len(st.session_state.user_history) + items_per_page - 1) // items_per_page

            # Display history items for the current page
            start_idx = (st.session_state.history_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            current_page_items = st.session_state.user_history[start_idx:end_idx]

            for i, item in enumerate(current_page_items):
                if st.sidebar.button(item[1], key=f"user_history_{i}"):
                    cookie_manager.set("target_history", json.dumps(item), key="set_target_history")
                    st.session_state.target_history = item
                    st.session_state.page = "history_summary"
                    #st.rerun()

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

    if search_term:
        content_match = db.search_content(search_term, st.session_state.id)
        summary_match = db.search_summary(search_term, st.session_state.id)
    else:
        st.warning("Please enter a search term.")
        content_match = []
        summary_match = []

    if content_match:
        st.markdown("**Content match**")
        for i, item in enumerate(content_match):
            if st.button(item[1], key=f"content_match_{i}"):
                cookie_manager.set("target_history", json.dumps(item), key="set_target_history")
                st.session_state.target_history = item
                st.session_state.page = "history_summary"
                #st.rerun()
    
    if summary_match:
        st.markdown("**Summary match**")
        for i, item in enumerate(summary_match):
            if st.button(item[1], key=f"summary_match_{i}"):
                cookie_manager.set("target_history", json.dumps(item), key="set_target_history")
                st.session_state.target_history = item
                st.session_state.page = "history_summary"
                #st.rerun()