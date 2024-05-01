import streamlit as st
import login
import add_order
import register
import add_service
import dashboard
# Define the sidebar
st.title("You Laundry Dashboard")
st.sidebar.title("Options")
page = st.sidebar.radio("Go to", ["Login", "Add Order","Add Service","Dashboard","Register"])

# Load the selected page
if page == "Login":
    #st.title("Home Page")
    login.main()
    # Add content for the home page
elif page == "Add Order":
    add_order.main()
    # Add content for Page 1
elif page== "Add Service":
    add_service.main()
elif page == "Register":
    register.main()
elif page == "Dashboard":
    dashboard.main()
    # Add content for Page 2
