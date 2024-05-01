import streamlit as st
import pymongo
from datetime import datetime, timedelta
import login
from db_conn import connect_to_mongodb

# Function to retrieve orders from the current month
def get_orders_current_month(db):
    print("getting orders for current month")
    # Get the start and end dates of the current month
    current_date = datetime.now()
    start_date = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = (current_date.replace(day=1) + timedelta(days=31)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    orders_collection = db['orders']
    print(f"displaying orders between {start_date} - {end_date}")
    # Query MongoDB to retrieve orders for the current month
    orders = orders_collection.find({
        "order_date": {"$gte": start_date, "$lt": end_date}
    })
    return list(orders)

# Function to display orders in a table
def display_orders(orders):
    if orders:
        st.table(orders)
    else:
        st.write("No orders found for the current month.")

# Main function
def main():
    login.get_logged_user()
    if login.st.session_state.loggedIn:
        st.title(f"Hello {login.st.session_state.loggedInUser}")
    else:
        st.warning("Please login first")
        st.stop()
    
    conn,db = connect_to_mongodb()
    st.title("Orders from Current Month")

    # Retrieve and display orders from the current month
    orders = get_orders_current_month(db)
    display_orders(orders)

if __name__ == "__main__":
    main()
