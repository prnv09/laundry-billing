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
    # start_date = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # end_date = (current_date.replace(day=1) + timedelta(days=31)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_date = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = current_date.replace(day=28) + timedelta(days=4)
    end_date = next_month - timedelta(days=next_month.day)
    orders_collection = db['orders']
    print(f"displaying orders between {start_date} - {end_date}")
    # Query MongoDB to retrieve orders for the current month
    orders = list(orders_collection.find({
        "order_date": {"$gte": start_date, "$lt": end_date}
    },{"service": 1, "customer_id": 1, "vendor_payment": 1, "remaining_amount": 1,"_id":0}))
    print(f"orders in current month - {list(orders)}")
    #orders_to_print = list(orders)
    return orders

# Function to display orders in a table
def display_orders(orders):
    #print(f"in display order function - {orders}")
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
    orders_to_print = get_orders_current_month(db)
    print(f"showing orders - {orders_to_print}")
    display_orders(orders_to_print)

if __name__ == "__main__":
    main()
