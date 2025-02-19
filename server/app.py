# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# from whisper_va import llm_result
# import json

# app = Flask(__name__)
# CORS(app)

# @app.route("/", methods=["GET"])
# def index():
#     # Retrieve input from query parameters
#     user_input = request.args.get("input", "")  # Default to an empty string if no input is provided
#     res = llm_result(user_input)
#     return jsonify({"message" : res})
# if __name__ == '__main__':
#     app.run(port = 8080)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import threading
from whisper_va import llm_result, mac_text_to_speech, record_audio
from pay import initiate_payment, check_phonepe_transaction_status
import uuid
import json
from flask_pymongo import PyMongo
from phonepe.sdk.pg.payments.v1.payment_client import PhonePeResponse


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ticket-page")
def ticket_page():
    return render_template("ticket.html")


order_id = None


def information():
    result = llm_result(
        """ summarise the whole ticket booking details by extracting the given information:
            do not add any comments using # 
        calculate the cost for the tickets 
        format:ex:
        {
  "order_amount": {
    "museum": "Chennai Museum",
    "location": "Chennai, Tamil Nadu",
    "tickets": {
      "adult": 2,
      "child": 1
    },
    "date": "12/12/24",
    "price": {
      "adult": 15,
      "child": 10
    },
    "discount": 40 (prune out '%' symbol)
    "total_cost": 40(should be integer only , do calculate (accurately do it ) and reduce the discount from their total bill and give integer output)
  }
}
        return the results as dictionary  
         """
    )
    print(result)
    l = result.find("{")
    r = result.rfind("}")
    result = json.loads(result[l : r + 1])
    cust_details = {
        "id": "cust001",
        "mobile": "7418857984",
        "name": "naveeth",
        "mail": "sec22ad081@sairamtap.edu.in",
    }
    print(result)
    print(type(result))
    if (
        "order_amount" in result.keys()
        and "total_cost" in result["order_amount"].keys()
    ):
        amount = result["order_amount"]["total_cost"]
    else:
        amount = 150
    recipt = {"id": order_id, "amount": amount}
    print(recipt)
    return cust_details, recipt


# order_id = None
# def information():
#     result = llm_result(
#         """ summarise the whole ticket booking details by extracting the given information:
#             do not add any comments using #
#         calculate the cost for the tickets
#         format:ex:
#         {
#     "museum": "Chennai Museum",
#     "location": "Chennai, Tamil Nadu",
#     "tickets": {
#       "adult": 2,
#       "child": 1
#     },
#     "date": "12/12/24",
#     "price": {
#       "adult": 15,
#       "child": 10
#     },
#     "total_cost": 40(should be integer only , do calculate and give integer output)

# }
#         return the results as dictionary
#          """
#                         )
#     print(result)
#     l = result.find('{')
#     r = result.rfind('}')
#     result = json.loads(result[l:r+1])
#     cust_details = {
#     "id": "cust001",
#     "mobile": "7418857984",
#     "name" : "naveeth",
#     "mail": "sec22ad081@sairamtap.edu.in"
#     }
#     print(result)
#     print(type(result))
#     recipt = {
#         "id": order_id,
#         "amount":result.total_cost if result.total_cost else 150
#     }
# return cust_details,recipt


@app.route("/process-message", methods=["POST"])
def process_message():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        llm_response = llm_result(user_message)
        is_booking = (
            "BOOK_NOW" in llm_response or "book_now" in llm_response
        )  # Check for booking response

        payment_session = None
        payment_link = None

        if is_booking:
            global order_id
            order_id = str(uuid.uuid4())
            cust_details, recipt = information()
            if "total_cost" in recipt.keys():
                total_cost = int(recipt["total_cost"])
            else:
                total_cost = 150

            payment_url = initiate_payment(order_id, cust_details, total_cost)
            response = {
                "response": llm_response,
                "is_payment": True,
                "payment_url": payment_url,
            }

        else:
            response = {"response": llm_response, "is_payment": False}

        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error in process_message: {e}")
        return jsonify({"error": "Failed to process message", "details": str(e)}), 500


# @app.route("/payment-success", methods=["POST"])
# def payment_success():
#     try:
#         data = request.json
#         payment_status = verify_payment(data.get("order_id"))

#         if payment_status == "success":
#             ticket_path = generate_ticket(order_id)
#             return jsonify({"payment_status": "success", "ticket_url": ticket_path})
#         else:
#             return jsonify({"payment_status": "failure"})
#     except Exception as e:
#         app.logger.error(f"Error processing payment status: {e}")
#         return jsonify({"error": "Failed to process payment status", "details": str(e)}), 500


@app.route("/process-audio", methods=["POST"])
def process_audio():
    try:
        audio_file = request.files.get("audio")
        if not audio_file:
            return jsonify({"error": "No audio file provided"}), 400

        # Save the uploaded audio file
        input_file_path = os.path.join("uploads", "inputs.wav")
        os.makedirs("uploads", exist_ok=True)
        audio_file.save(input_file_path)

        # Step 1: Transcribe Audio
        transcription = record_audio(input_file_path)
        app.logger.info(f"Transcription: {transcription}")

        # Step 2: Generate LLM Response
        llm_response = llm_result(transcription)
        payment_session = None
        payment_link = None
        is_booking = "BOOK_NOW" in llm_response
        if is_booking:
            cust_details, recipt = information()
            payment_session = initiate_payment(cust_details, recipt)
            payment_link = (
                f"https://checkout.cashfree.com?session_id={payment_session}"
                if payment_session
                else None
            )
        app.logger.info(f"LLM Response: {llm_response}")

        # Step 3: Text-to-Speech (optional)
        threading.Thread(target=mac_text_to_speech, args=(llm_response,)).start()

        # Cleanup
        os.remove(input_file_path)

        # Return transcription and response
        response = {
            "transcription": transcription,
            "bot_response": llm_response,
            "is_payment": is_booking,
            "payment_session": payment_session,
        }
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error in process_audio: {e}")
        return jsonify({"error": "Failed to process audio", "details": str(e)}), 500


@app.route("/check_phonepe_status", methods=["POST"])
def check_phonepe_status():
    data = request.get_json()
    if not data or "unique_transaction_id" not in data:
        return jsonify({"error": "unique_transaction_id is required"}), 400
    unique_transaction_id = data["unique_transaction_id"]
    response = check_phonepe_transaction_status(unique_transaction_id)

    # Ensure the response is in a valid format for Flask
    if isinstance(response, PhonePeResponse):
        # Convert PhonePeResponse to dict or format as needed
        response_dict = {
            "success": response.success,
            "code": response.code,
            "message": response.message,
            "data": (
                response.data.__dict__
                if hasattr(response.data, "__dict__")
                else response.data
            ),
        }
        return jsonify(response_dict), 200
    else:
        return jsonify({"error": "Invalid response from PhonePe API"}), 500


# @app.route('/payment-success', methods=["POST"])
# def process_payment_status():
#     try:
#           # Assume the frontend sends some payload
#         payment_status = paid_status(order_id)  # success/failure
#         ticket_path = "museum_ticket.pdf" if payment_status == "success" else None
#         print(payment_status)
#         return jsonify({
#             "payment_status": payment_status,
#             "ticket_path": ticket_path
#         })
#     except Exception as e:
#         app.logger.error(f"Error processing payment status: {e}")
#         return jsonify({"error": "Failed to process payment status"}), 500

# MongoDB configuration
app.config["MONGO_URI"] = (
    "mongodb+srv://hariprashaad:HariSR035@cluster0.gjdgj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Initialize PyMongo
mongo = PyMongo(app)


@app.route("/add-ticket", methods=["POST"])
def add_ticket():
    try:
        data = (
            request.json
        )  # Example: {"museum": "Chennai Museum", "location": "Chennai", "tickets": {"adult": 2, "child": 1}}
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Insert data into the "Tickets" collection
        mongo.db.Tickets.insert_one(data)
        return jsonify({"message": "Ticket data added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#  Retrieve all data from the Tickets collection
# @app.route("/list-tickets", methods=["GET"])
# def list_tickets():
#     try:
#         # Fetch data from the "Tickets" collection
#         tickets = list(mongo.db.Tickets.find({}, {"_id": 0}))  # Omit "_id" from results
#         return jsonify(tickets), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# from db import add_ticket_final, add_transaction, add_user
# import os
# import threading
# import uuid
# from whisper_va import llm_result, mac_text_to_speech
# from flask_pymongo import PyMongo
# from pay import initiate_payment, verify_payment
# from tickets import generate_ticket

# app = Flask(__name__)
# # app.config["MONGO_URI"] = "mongodb+srv://hariprashaad:HariSR035@cluster0.gjdgj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# # mongo = PyMongo(app)
# import json
# order_id = None
# order_id = None
# ticket_info = {}
# def information():
#     result = llm_result(
#         """ summarise the whole ticket booking details by extracting the given information:
#             do not add any comments using #
#         calculate the cost for the tickets
#         format:ex:
#         {
#   "order_amount": {
#     "museum": "Chennai Museum",
#     "location": "Chennai, Tamil Nadu",
#     "tickets": {
#       "adult": 2,
#       "child": 1
#     },
#     "date": "12/12/24",
#     "price": {
#       "adult": 15,
#       "child": 10
#     },
#     "total_cost": 40(should be integer only , do calculate and give integer output)
#   }
# }
#         return the results as dictionary
#          """
#                         )
#     print(result)
#     l = result.find('{')
#     r = result.rfind('}')
#     result = json.loads(result[l:r+1])
#     cust_details = {
#     "id": "cust001",
#     "mobile": "7418857984",
#     "name" : "naveeth",
#     "mail": "sec22ad081@sairamtap.edu.in"
#     }
#     print(result)
#     print(type(result))
#     print(result['order_amount']['total_cost'])
#     recipt = {
#         "id": order_id,
#         "amount":result['order_amount']['total_cost']
#     }
#     # print(recipt)
#     return cust_details,recipt

# @app.route("/", methods=["GET"])
# def index():
#     return render_template("index.html")

# @app.route("/ticket/", methods=["GET"])
# def indexx():
#     return render_template("ticket.html")


# @app.route("/process-message", methods=["POST"])
# def process_message():
#     try:
#         user_message = request.json.get("message")
#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         llm_response = llm_result(user_message)
#         is_booking = "BOOK_NOW" in llm_response or "BOOK NOW" in llm_response

#         if is_booking:
#             global order_id
#             order_id = str(uuid.uuid4())

#             # Example customer and booking details
#             # cust_details = {
#             #     "id": "cust001",
#             #     "mobile": "7418857984",
#             #     "name": "naveeth",
#             #     "email": "example@example.com"
#             #                 }
#             # booking_details = {
#             #     "museum": "Chennai Museum",
#             #     "location": "Chennai, Tamil Nadu",
#             #     "date": "12/12/2024",
#             #     "tickets": {"adult": 2, "child": 1},
#             #     "total_cost": 500000
#             # }
#             cust_details,recipt = information()

#             # Save booking details to DB
#             # mongo.db.Tickets.insert_one(booking_details)

#             # Initiate payment
#             payment_url = initiate_payment(order_id, cust_details, int(recipt["total_cost"])*100)
#             response = {
#                 "response": llm_response,
#                 "is_payment": True,
#                 "payment_url": payment_url
#             }
#             ticket_info = jsonify(ticket_info)

#         else:
#             response = {"response": llm_response, "is_payment": False}

#         return jsonify(response)
#     except Exception as e:
#         app.logger.error(f"Error in process_message: {e}")
#         return jsonify({"error": "Failed to process message", "details": str(e)}), 500

# # @app.route("/payment-success", methods=["POST"])
# # def payment_success():
# #     try:
# #         data = request.json
# #         payment_status = verify_payment(data.get("order_id"))

# #         if payment_status == "success":
# #             ticket_path = generate_ticket(order_id)
# #             return jsonify({"payment_status": "success", "ticket_url": ticket_path})
# #         else:
# #             return jsonify({"payment_status": "failure"})
# #     except Exception as e:
# #         app.logger.error(f"Error processing payment status: {e}")
# #         return jsonify({"error": "Failed to process payment status", "details": str(e)}), 500


# @app.route('/api/tickets/add', methods=['POST'])
# def addTickets():
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     user_data = request.get_json()
#     success = add_ticket_final(user_data)

#     if success:
#         return jsonify({"message": "User added successfully"}), 201
#     else:
#         return jsonify({"error": "Failed to add user"}), 500


# @app.route('/api/transaction/add', methods=['POST'])
# def addTransactions():
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     user_data = request.get_json()
#     success = add_transaction(user_data)

#     if success:
#         return jsonify({"message": "User added successfully"}), 201
#     else:
#         return jsonify({"error": "Failed to add user"}), 500


# @app.route('/api/user/auth', methods=['POST'])
# def userAuth():
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     user_data = request.get_json()
#     success = add_user(user_data)

#     if success:
#         return jsonify({"message": "User added successfully"}), 201
#     else:
#         return jsonify({"error": "Failed to add user"}), 500


# def getDetails():
#     return ticket_info

# if __name__ == "__main__":
#     app.run(host="0.0.0.0",port=5000)
