from db_conn import connect_to_mongodb
import streamlit as st
import login

def main():
    login.get_logged_user()
    if login.st.session_state.loggedIn:
        st.title(f"Hello {login.st.session_state.loggedInUser}")
    else:
        st.warning("Please login first")
        st.stop()
    
    conn,db = connect_to_mongodb()
    yl_services = db['yl-services']
    tbc_services = db['tbc-services']
    service_name = st.text_input("Service Name")
    service_price = st.number_input("Price")
    new_service = {
            service_name:service_price
        }
    #st.number_input("Commission")
    if st.button("Add YouLaundry service"):
        yl_services.update_many({"owner":login.st.session_state.loggedInUser},{"$set":new_service})
        st.success("Service added into youlaundry")
    if st.button("Add Vendor service"):
        tbc_services.update_many({"owner":login.st.session_state.loggedInUser},{"$set":new_service})
        st.success("Service added into vendor")

