import streamlit as st
from db_instance import db
import time

def first_preference_page(cookie_manager):
    cookie_manager.set("current_page", "first_preference", key="set_current_page")

    st.title("Set Your Preferences")
    st.markdown("### Customize your experience")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create a New Preference", use_container_width=True, key="create_new_preference"):
            st.session_state.using_preference = None
            st.session_state.page = "second_preference_page"
            st.rerun()
    with col2:
        if st.session_state.user_preferences:
            name_values = [item["name"] for item in st.session_state.user_preferences if "name" in item]
        else:
            name_values = []
        select = st.selectbox("Select an existing preference", name_values if name_values else ["No preferences available"], index=0)
        if st.button("Confirm", use_container_width=True, key="edit_preference_button"):
            if select != "No preferences available":
                target_preference = next((item for item in st.session_state.user_preferences if item["name"] == select), None)
                st.session_state.using_preference = target_preference
                st.session_state.page = "second_preference_page"
                st.rerun()
            else:
                st.warning("No preferences available. Please create a new preference.")
    
    st.markdown("---")
    if st.button("Back", use_container_width=True, key="back_to_home"):
        st.session_state.page = "home"
        st.rerun()

def second_preference_page(selected_preference=None, name_values=None):
    if selected_preference:
        st.markdown(f"### Edit Your Preference:")
    else:
        st.markdown("### Create a New Preference:")

    print(selected_preference)
    name = st.text_input("Give your preference a name", value=selected_preference['name'] if selected_preference else "")
    temperature = st.slider("Temperature", 0.0, 1.0, selected_preference["temperature"] if selected_preference else 0.5)
    max_tokens = st.slider("Max Tokens", 1, 500, selected_preference["max_tokens"] if selected_preference else 100)

    styles = ["Formal", "Casual", "Technical"]
    default_index = styles.index(selected_preference["style"]) if selected_preference else 0
    style = st.selectbox("Select a style", ["Formal", "Casual", "Technical"], index=default_index)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Preference", use_container_width=True, key="save_preference"):
            if name:
                preference = {
                    "name": name,
                    "style": style,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                # Save the preference to the database
                if name in name_values:
                    for i, pref in enumerate(st.session_state.user_preferences):
                        if pref["name"] == name:
                            del st.session_state.user_preferences[i]
                            st.session_state.user_preferences.append(preference)
                            break
                else:
                    if st.session_state.user_preferences:
                        st.session_state.user_preferences.append(preference)
                    else:
                        st.session_state.user_preferences = [preference]
                db.save_user_preference(st.session_state.id, st.session_state.user_preferences)
                # Update session state
                st.session_state.using_preference = preference
                st.session_state.page = "summarization"
                st.success("Preference saved successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please enter a preference name.")
    with col2:
        if st.button("Use This Preference only Once", use_container_width=True, key="use_once"):
            preference = {
                    "name": name,
                    "style": style,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            st.session_state.using_preference = selected_preference
            st.session_state.page = "summarization"
            st.rerun()
    
    st.markdown("---")
    if st.button("Back", use_container_width=True, key="back_to_first_preference"):
        st.session_state.page = "first_preference"
        st.rerun()