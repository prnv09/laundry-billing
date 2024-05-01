import pymongo
from passlib.hash import bcrypt
import db_conn
import streamlit as st
from passlib.hash import bcrypt
import time
# Connect to MongoDB
client,db = db_conn.connect_to_mongodb() 

users_collection = db["users"]

# Register a new user (store hashed password)
def register_user(username, password):
    hashed_password = bcrypt.hash(password)
    user_data = {
        "username": username,
        "password": hashed_password,
        "status":"pending"
    }
    users_collection.insert_one(user_data)
    st.success("Registered Successfully! your account needs to be approved.")

# Authenticate a user

def clear_box():
    #time.sleep(5)
    st.session_state['username']=''
    st.session_state.username= ""
    st.session_state.password = ""



# Example usage

# is_authenticated = authenticate_user("user1", "password123")
# print("Is authenticated:", is_authenticated)
def main():
    st.title("Register Page")
    with st.form(key="logregister_form",clear_on_submit=True):
        # if "username" not in st.session_state:
        #     st.session_state.username = ""
        # if "password" not in st.session_state:
        #     st.session_state.password = ""
        # Input fields for username and password
        # st.session_state['username']= st.text_input("Username")
        # st.session_state['password'] = st.text_input("Password", type="password")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Register")
    
    # Login button
        if submit_button:
            #register_user(st.session_state['username'], st.session_state['password'])
            register_user(username, password)

        #clear_box()

if __name__ == "__main__":
    main()