import streamlit as st
import extra_streamlit_components as stx
import time
import json

from db_instance import db
from user import login_page, signup_page, welcome_page
from home import home_page
from preference import first_preference_page, second_preference_page, delete_preferences_page
from summarization import summarization_page, history_summary_page

print("I am top")
cookie_manager = stx.CookieManager()
#cookie_manager.delete("current_page", key="whatever")

# Initialize session state
if 'id' not in st.session_state:
    st.session_state.id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'using_preference' not in st.session_state:
    st.session_state.using_preference = None
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = None
if 'user_history' not in st.session_state:
    st.session_state.user_history = None
if 'target_history' not in st.session_state:
    st.session_state.target_history = None
if 'refresh' not in st.session_state:
    st.session_state.refresh = True
if 'target_history' not in st.session_state:
    st.session_state.target_history = None

print(st.session_state)
cookies = cookie_manager.get_all()
# Wait for cookies to load
if not cookies:
    st.warning("Waiting for cookies to load...")
    st.stop()
print(cookies)

if st.session_state.id is None and st.session_state.username is None:
    if "user_db_id" in cookies and "user_db_name" in cookies and st.session_state.refresh:
        st.session_state.id = cookies["user_db_id"]
        st.session_state.username = cookies["user_db_name"]
        if "using_preference" in cookies:
            st.session_state.using_preference = cookies["using_preference"]
        else:
            st.session_state.using_preference = None
        if "target_history" in cookies:
            st.session_state.target_history = tuple(cookies["target_history"])
        else:
            st.session_state.target_history = None
        st.session_state.user_preferences = db.get_user_preferences(st.session_state.id)
        st.session_state.user_history = db.get_user_history(st.session_state.id)
        if "current_page" in cookies:
            print("I am here 2")
            st.session_state.page= cookies["current_page"]
        else:
            st.session_state.page = "home"
        st.session_state.refresh = False
    elif "page" not in st.session_state:
        print("been here")
        st.session_state.page = "welcome"

print("DB: ", db.get_user(st.session_state.id))
#print("User History:", db.get_all_history())

print(st.session_state.page)
if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "login":
    login_page(cookie_manager)
elif st.session_state.page == "signup":
    signup_page(cookie_manager)
elif st.session_state.page == "home":
    home_page(cookie_manager)
elif st.session_state.page == "first_preference":
    first_preference_page(cookie_manager)
elif st.session_state.page == "summarization":
    summarization_page(cookie_manager)
elif st.session_state.page == "second_preference_page":
    if st.session_state.user_preferences:
        name_values = [item["name"] for item in st.session_state.user_preferences if "name" in item]
    else:
        name_values = []
    second_preference_page(cookie_manager, st.session_state.using_preference, name_values)
elif st.session_state.page == "delete_preferences":
    delete_preferences_page(cookie_manager)
elif st.session_state.page == "history_summary":
    history_summary_page(cookie_manager, st.session_state.target_history)
else:
    st.session_state.page = "welcome"
