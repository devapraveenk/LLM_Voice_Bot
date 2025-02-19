from flask import Flask, render_template, request, jsonify
from db import add_ticket_final, add_transaction, add_user
app = Flask(__name__)



@app.route('/api/tickets/add', methods=['POST'])
def addTickets():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    user_data = request.get_json()
    success = add_ticket_final(user_data)

    if success:
        return jsonify({"message": "User added successfully"}), 201
    else:
        return jsonify({"error": "Failed to add user"}), 500

    
@app.route('/api/transaction/add', methods=['POST'])
def addTransactions():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    user_data = request.get_json()
    success = add_transaction(user_data)

    if success:
        return jsonify({"message": "User added successfully"}), 201
    else:
        return jsonify({"error": "Failed to add user"}), 500
    


@app.route('/api/user/auth', methods=['POST'])
def userAuth():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    user_data = request.get_json()
    success = add_user(user_data)

    if success:
        return jsonify({"message": "User added successfully"}), 201
    else:
        return jsonify({"error": "Failed to add user"}), 500



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
