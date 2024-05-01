import streamlit as st
import db_conn
from passlib.hash import bcrypt
# Function to authenticate user

if 'loggedIn' not in st.session_state:
    st.session_state.loggedIn = False
def authenticate_user(username, password):
    client,db = db_conn.connect_to_mongodb()
    users_collection = db.users
    user_data = users_collection.find_one({"username": username})
    if user_data:
        print("User Found--------")
        if user_data["status"]=="active":
            print("User is Active ------")
            hashed_password = user_data["password"]
            
            if bcrypt.verify(password, hashed_password):
                print("Password matched, logging in -------")
                st.session_state.loggedInUser = user_data['username']
                st.session_state.loggedIn = True
                return True
        else:
            st.warning("Your account is not active yet.")
            return False
    return False

def get_logged_user():
    print("getting logged in user info")
    if 'loggedIn' not in st.session_state:
        print("assigning session variable to check loggedin or not")
        st.session_state.loggedIn = False
    if st.session_state.loggedIn:
        print(f"user logged in, returning username {st.session_state.loggedInUser}")
        return True,st.session_state.loggedInUser
    else:
        return False

# Streamlit UI
def main():
    st.title("Login Page")
    
    # Input fields for username and password
    with st.form(key="login_form",clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")
    # Login button
        if submit_button:
            if authenticate_user(username, password):
                st.success("Login successful!")
                # Redirect to main window or dashboard
                
            else:
                st.error("Invalid username or password")

if __name__ == "__main__":
    main()
