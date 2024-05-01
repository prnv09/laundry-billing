# input - weight, customer_bill, service_Select,discount,tbc_variable_price
# 
# process - 1) select service
# 2)enter customer_id - last 4 digit 
# 3)enter weight
# 4)enter customer_bill
# 5)select tbc_price if variable - enter it 
 
import datetime
from db_conn import connect_to_mongodb
import streamlit as st
import login
# Define a dictionary for fixed service costs
tbc_price_list = {}
order ={}
yl_price_list={}
conn,db = connect_to_mongodb()
def get_tbc_price_list():
    #print(conn,db)
    #print(f"available collections - {db.list_collection_names()}")
    tbc_services_collection = db["tbc-services"]
    tbc_services = tbc_services_collection.find_one()
    for key,value in tbc_services.items():
        tbc_price_list[key]=value
    tbc_price_list.pop("_id")
    #print(f"tbc_services -- {tbc_services}")

#Function to calculate vendor payment and remaining amount
def calculate_payment(tbc_price,weight,customer_bill):
    print(f"tbc price - {tbc_price}")
    tbc_discount = tbc_price * 0.37
    order["tbc_discount"] = tbc_discount
    print(f"tbc discount {tbc_discount}")
    tbc_cost = tbc_price - tbc_discount
    order["tbc_cost"]= tbc_cost
    print(f"tbc_cost - {tbc_cost}")
    vendor_payment = tbc_cost * weight
    order["vendor_payment"]=vendor_payment
    print(f"total vendor payment {tbc_cost}*{weight}: {vendor_payment}")
    remaining_amount = customer_bill - vendor_payment
    order["remaining_amount"]=remaining_amount
    print(f"remaining amount - {remaining_amount}")
    return vendor_payment, remaining_amount

def calculate_customer_bill(wt,service,discount_per,discount_val):
    yl_services_collection = db["yl-services"]
    yl_services = yl_services_collection.find_one()
    for key,value in yl_services.items():
        yl_price_list[key]=value
    yl_price_list.pop("_id")
    customer_bill = yl_price_list[service] * wt 
    if discount_per>0:
        discount_value = (customer_bill/100)*discount_per
        customer_bill = customer_bill-discount_value
    elif discount_val>0:
        customer_bill= customer_bill-discount_val
    order["customer_bill"]= customer_bill
    order['yl_service_cost'] = yl_price_list[service]
    print(f"Customer bill = {customer_bill}")
     

# Function to display order details
def display_order(order):
    st.write("Order ID:", order["order_id"])
    st.write("Service:", order["service"])
    #st.write("Service Cost:", order["tbc_price"])
    st.write("Vendor Payment:", order["vendor_payment"])
    st.write("Remaining Amount:", order["remaining_amount"])
    st.write("---")

def generate_order_id():
    # Get current date and time
    current_datetime = datetime.datetime.now()
    
    # Format date as dd-mm-yy
    date_str = current_datetime.strftime("%d-%m-%y")
    
    # Format time as hh-mm
    time_str = current_datetime.strftime("%H-%M-%S")
    
    # Extract last 4 digits of customer ID
    last_4_digits = str(order['customer_id'])[-4:]
    
    # Concatenate date, time, and last 4 digits of customer ID to generate order ID
    order_id = f"{date_str.replace('-','')}{time_str.replace('-','')}{last_4_digits}"
    print(f"order ID generated - {order_id}")
    return order_id

def insert_record(obj,cln_name):
    collection = db[cln_name]
    result= collection.insert_one(obj)
    print(f"Inserted data in to database, Insert ID - {result.inserted_id}")
#Main function to run the app
def main():
    # st.title("Laundry Order Tracker")
    login.get_logged_user()
    if login.st.session_state.loggedIn:
        st.title(f"Hello {login.st.session_state.loggedInUser}")
    else:
        st.warning("Please login first")
        st.stop()

    #orders = []
    get_tbc_price_list()
    #while True:
    st.subheader("Add New Order")
    customer_id = st.text_input("Enter Customer ID:",key="customer_id")
    service = st.selectbox("Select Service:", list(tbc_price_list.keys()),key="service")
    order['service']=service
    # print(tbc_price_list)
    # print(tbc_price_list.keys())
    weight = st.number_input("Enter weight/quantity",min_value=1,key="weight")
    order["weight"] = weight
    
    # is_discount_per = st.checkbox("Discount given in % ?",key="is_discount_per")
    # is_discount_val = st.checkbox("Discount given in rupees ?",key="is_discount_val")
 
    is_discount_per, is_discount_val = st.columns(2)

# Add checkboxes in a horizontal layout
    with is_discount_per:
        #option1 = st.checkbox("Discount given in % ?",key="is_discount_per")
        discount_per = st.number_input("discount in %")
    with is_discount_val:
        #option2 = st.checkbox("Discount given in rupees ?",key="is_discount_val")
        discount_val = st.number_input("discount in rupees")

    is_variable = st.checkbox("Variable cost?",key="is_variable")
    if is_variable:
        custom_service = st.text_input("Enter Service Name")
        order['service']=custom_service
        tbc_price = st.number_input("Enter TBC price for one quantity:", min_value=0.0,key="variable_service_cost")
        yl_price_variable = st.number_input("Enter YL bill for one quantity",key="customer_bill")
        order['yl_service_cost'] = yl_price_variable
        order["customer_bill"] = yl_price_variable * weight
        
    else:
        tbc_price = tbc_price_list[service]
        
        calculate_customer_bill(weight,service,discount_per,discount_val)
    if st.button("Add Order"):
        order['owner'] = login.st.session_state.loggedInUser
        order['customer_id'] = customer_id
        order['order_id'] = generate_order_id()
        order['tbc_price'] = tbc_price
        vendor_payment, remaining_amount = calculate_payment(tbc_price,weight,order['customer_bill'])
        current_date_str = datetime.datetime.now().strftime("%d-%m-%y")
        order['order_date'] = datetime.datetime.now()
        insert_record(order,'orders')
        st.write('Total Received Amount: ', order["customer_bill"])
        st.write('Payment to Vendor: ',order["vendor_payment"])
        st.write('Profit on order: ',order["remaining_amount"])
        # if tbc_price:
        #     vendor_payment, remaining_amount = calculate_payment(tbc_price,weight,customer_bill)
        # else:
        #     vendor_payment, remaining_amount = calculate_payment(tbc_price,weight,customer_bill)
        # orders.append({
        #     "order_id": order_id,
        #     "service": service,
        #     "tbc_price": tbc_price,
        #     "vendor_payment": vendor_payment,
        #     "remaining_amount": remaining_amount
        # })
    #st.subheader("Orders List")
    # for order in orders:
    #     display_order(order)



if __name__ == "__main__":
    main()

# get_tbc_price_list()
# print(tbc_price_list)