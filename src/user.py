import streamlit as st
import time
from db_instance import db

# Define callback functions
def go_to_login():
    st.session_state.page = "login"

def go_to_signup():
    st.session_state.page = "signup"

def go_to_welcome():
    st.session_state.page = "welcome"

def welcome_page():
    st.title("Welcome to our text summarizer!")
    st.button("Log in", on_click=go_to_login)
    st.button("Sign up", on_click=go_to_signup)

def login_page(cookie_manager):
    st.title("Login")
    username = st.text_input("Username")
    
    if st.button("Login"):
        if username:
            id = db.user_exists(username)
            if id:
                try:
                    # Set cookies with unique keys
                    cookie_manager.set("user_db_id", str(id), key="set_user_db_id")
                    cookie_manager.set("user_db_name", username, key="set_username_cookie")
                    
                    # Update session state
                    st.session_state.id = str(id)
                    st.session_state.username = username
                    # pull user preferences from db
                    st.session_state.user_preferences = db.get_user_preferences(id) #list of dict

                    st.session_state.page = "home"              
                except Exception as e:
                    print(f"Error setting cookies: {e}")
                    st.error(f"Error setting cookies: {e}")
            else:
                st.error("Username not found. Please sign up.")
        else:
            st.error("Please enter a username.")
    st.button("I don't have an account", on_click=go_to_signup)
    st.button("Back", on_click=go_to_welcome)

def signup_page(cookie_manager):
    st.title("Sign Up")
    username = st.text_input("Enter your username")

    if st.button("Sign Up"):
        if username:
            id = db.add_user(username)

            # Set cookies
            cookie_manager.set("user_db_id", str(id), key="set_user_db_id")
            cookie_manager.set("user_db_name", username, key="set_username_cookie")

            st.session_state.id = str(id)
            st.session_state.username = username
            st.session_state.user_preferences = db.get_user_preferences(id)
            st.session_state.page = "home"

            #st.rerun()
        else:
            st.error("Please enter a username.")
    st.button("Already have an account?", on_click=go_to_login)
    st.button("Back", on_click=go_to_welcome)

def logout(cookie_manager):
    # Clear cookies
    try:
        cookie_manager.delete("user_db_name", key="delete_username_cookie")
        
    except Exception as e:
        print(f"Error deleting cookies: {e}")
        st.error(f"Error deleting cookies: {e}")
    try:
        cookie_manager.delete("user_db_id", key="delete_user_db_id")
    except Exception as e:
        print(f"Error deleting cookies: {e}")
        st.error(f"Error deleting cookies: {e}")
    try:
        cookie_manager.delete("current_page", key="delete_user_db_id")
    except Exception as e:
        print(f"Error deleting cookies: {e}")
        st.error(f"Error deleting cookies: {e}")
    st.session_state.clear()
    st.session_state.page = "welcome"
    time.sleep(0.5)
    st.rerun()