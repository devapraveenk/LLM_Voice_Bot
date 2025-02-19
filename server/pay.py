import uuid
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from phonepe.sdk.pg.env import Env
import requests
# from app import getDetails

import json

# def transform_json(data):
#     # Extract relevant information from the input data
#     museum = data['museum']
#     location = data['location']
#     adult_count = data['tickets']['adult']
#     child_count = data['tickets']['child']
#     date = data['date']
#     adult_price = data['price']['adult']
#     total_cost = data['total_cost']

#     # Calculate child price based on adult price (assuming a fixed ratio)
#     child_price = 20  # Adjust this as needed

#     # Create the transformed JSON data
#     transformed_data = {
#         "museum": museum,
#         "location": location,
#         "adult": adult_count,
#         "child": child_count,
#         "date": date,
#         "adult_price": adult_price,
#         "child_price": child_price,
#         "total_cost": total_cost
#     }

#     return transformed_data


# Create the Pay Page request
def initiate_payment(order_id, cust_details, amount):

        # Configuration
    merchant_id = "SANDBOXTESTMID"  # Replace with your Merchant ID
    salt_key = "51778fc0-016b-48fe-b509-108277bfa5e2"  # Replace with your Salt Key
    salt_index = 1  # Replace with your Salt Index
    # env = "https://sandbox.phonepe.com"  # Use sandbox for testing, change to production URL when live
    env=Env.UAT

    # Initialize the PhonePe client
    phonepe_client = PhonePePaymentClient(
        merchant_id=merchant_id,
        salt_key=salt_key,
        salt_index=salt_index,
        env=env,
        should_publish_events=True
    )


    # Generate unique transaction details
    unique_transaction_id = str(uuid.uuid4()) # Unique ID for this transaction
    ui_redirect_url = "http://localhost:3000/ticket?unique_transaction_id="+str(unique_transaction_id)  # Redirect URL for the user
    s2s_callback_url = "https://www.merchant.com/callback"  # Server-to-server callback URL
    #amount = 50000  # Amount in paise (100 paise = 1 INR)
    merchant_user_id = cust_details["id"]  # Unique user ID assigned by the merchant


    pay_page_request = PgPayRequest.pay_page_pay_request_builder(
        merchant_transaction_id=unique_transaction_id,
        amount=amount*100,
        merchant_user_id=merchant_user_id,  # User ID assigned by merchant
        callback_url=s2s_callback_url,
        redirect_url=ui_redirect_url
    )
    # Send payment request
    pay_page_response = phonepe_client.pay(pay_page_request)
    print(pay_page_response)
    pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
    return(pay_page_url)

# initiate_payment(1,{'id':'1'}, )
    # details = getDetails()
    # output_data = transform_json(result['order_amount'])
    # output_data['user_id'] = 'hari'
    # output_data['transaction_id'] = unique_transaction_id
    # output_data['ticket_status'] = 'started'
    # output_data['phone_num'] = '393939333'
    # requests.post('/api/transaction/add', output_data)
    



def check_phonepe_transaction_status(unique_transaction_id):
            # Configuration
    merchant_id = "SANDBOXTESTMID"  # Replace with your Merchant ID
    salt_key = "51778fc0-016b-48fe-b509-108277bfa5e2"  # Replace with your Salt Key
    salt_index = 1  # Replace with your Salt Index
    # env = "https://sandbox.phonepe.com"  # Use sandbox for testing, change to production URL when live
    env=Env.UAT

    # Initialize the PhonePe client
    phonepe_client = PhonePePaymentClient(
        merchant_id=merchant_id,
        salt_key=salt_key,
        salt_index=salt_index,
        env=env,
        should_publish_events=True
    )
    print(phonepe_client)

    response = phonepe_client.check_status(unique_transaction_id)
    print(response)
    
    return response    










    



# initiate_payment(1, {"id":"1"}, 10)

def verify_payment(order_id):
    status = phonepe_client.get_payment_status(order_id)
    if status.success:
        return "success"
    else:
        return "failure"

# try:
#     # Initiate the payment
#     pay_page_response = phonepe_client.pay(pay_page_request)

#     if pay_page_response.success:
#         # Extract and display the redirect URL for the user
#         pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
#         print("Redirect the user to:", pay_page_url)
#     else:
#         # Handle the error if the response indicates failure
#         print("Payment initialization failed.")
#         print("Error Code:", pay_page_response.code)
#         print("Error Message:", pay_page_response.message)

# except Exception as e:
#     # Handle exceptions during the payment request process
#     print("An error occurred while initiating the payment:", str(e))


# from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
# from phonepe.sdk.pg.env import Env
# import uuid

# merchant_id = "SANDBOXTESTMID"
# salt_key = "51778fc0-016b-48fe-b509-108277bfa5e2"
# salt_index = 1
# env = Env.UAT

# phonepe_client = PhonePePaymentClient(
#     merchant_id=merchant_id,
#     salt_key=salt_key,
#     salt_index=salt_index,
#     env=env,
# )

# def initiate_payment(order_id, cust_details, amount):
#     redirect_url = f"http://localhost:5000/payment-success"
#     request = phonepe_client.pay_page_pay_request_builder(
#         merchant_transaction_id=order_id,
#         amount=int(amount) * 100,
#         merchant_user_id=cust_details.id,  # User ID assigned by merchant
#         # callback_url=s2s_callback_url,
#         redirect_url=redirect_url

        
#         # order_id=order_id,
#         # amount=,
#         # customer_data=cust_details,
#         # callback_url=callback_url,
#     )
#     return request.payment_url

