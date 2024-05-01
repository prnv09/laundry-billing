import streamlit as st
import login
import add_order
import register
# Define the sidebar
st.title("You Laundry Dashboard")
st.sidebar.title("Options")
page = st.sidebar.radio("Go to", ["Login", "Add Order", "Register"])

# Load the selected page
if page == "Login":
    #st.title("Home Page")
    login.main()
    # Add content for the home page
elif page == "Add Order":
    add_order.main()
    # Add content for Page 1
elif page == "Register":
    register.main()
    # Add content for Page 2
