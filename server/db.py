import sqlite3
import uuid

def add_ticket_final(person):
    # Step 1: Create or connect to a SQLite database
    try:
        values = list(person.values())
        (user_id, transaction_id, phone_num, museum, location, adult, child, date, adult_price, child_price, total_cost) = person.values()
        print((user_id, transaction_id, phone_num, museum, location, adult, child, date, adult_price, child_price, total_cost))
        
        conn = sqlite3.connect('database/tickets.db')
        cursor = conn.cursor()

        # Step 2: Create a table (if not already exists)
        cursor.execute('''CREATE TABLE IF NOT EXISTS ticket_info
                        (user_id TEXT, transaction_id TEXT, phone_num TEXT, museum TEXT, location TEXT, 
                        adult INTEGER, child INTEGER, date TEXT, 
                        adult_price INTEGER, child_price INTEGER, total_cost INTEGER)''')

        # Step 3: Dictionary to insert
        ticket_dict = {
            "user_id": user_id,
            "transaction_id": transaction_id,
            "phone_num": phone_num,
            "museum": museum,
            "location": location,
            "adult": adult,
            "child": child,
            "date": date,
            "adult_price": adult_price,
            "child_price": child_price,
            "total_cost": total_cost
        }

        # Step 4: Insert dictionary items into the table
        cursor.execute('''INSERT INTO ticket_info (user_id, transaction_id, phone_num, museum, location, 
                    adult, child, date, adult_price, child_price, total_cost) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (ticket_dict["user_id"], ticket_dict["transaction_id"], ticket_dict["phone_num"], ticket_dict["museum"], 
                 ticket_dict["location"], ticket_dict["adult"], ticket_dict["child"], 
                 ticket_dict["date"], ticket_dict["adult_price"], ticket_dict["child_price"], ticket_dict["total_cost"]))


        # Step 5: Commit and close the connection
        conn.commit()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def add_transaction(person):
    # Step 1: Create or connect to a SQLite database
    try:
        values = list(person.values())
        print(values, len(values))
        (user_id, transaction_id, transaction_status, ticket_status, phone_num, museum, location, adult, child, date, adult_price, child_price, total_cost) = person.values()
        print((user_id, transaction_id, transaction_status, ticket_status,phone_num, museum, location, adult, child, date, adult_price, child_price, total_cost))
        
        conn = sqlite3.connect('database/tickets.db')
        cursor = conn.cursor()

        # Step 2: Create a table (if not already exists)
        cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_info
                        (user_id TEXT, transaction_id TEXT,transaction_status TEXT, ticket_status TEXT, phone_num TEXT, museum TEXT, location TEXT, 
                        adult INTEGER, child INTEGER, date TEXT, 
                        adult_price INTEGER, child_price INTEGER, total_cost INTEGER)''')

        # Step 3: Dictionary to insert
        ticket_dict = {
            "user_id": user_id,
            "transaction_id": transaction_id,
            "transaction_status" : transaction_status, 
            "ticket_status" : ticket_status,
            "phone_num": phone_num,
            "museum": museum,
            "location": location,
            "adult": adult,
            "child": child,
            "date": date,
            "adult_price": adult_price,
            "child_price": child_price,
            "total_cost": total_cost
        }

        # Step 4: Insert dictionary items into the table
        cursor.execute('''INSERT INTO transaction_info (user_id, transaction_id,transaction_status, ticket_status, phone_num, museum, location, 
                    adult, child, date, adult_price, child_price, total_cost) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (ticket_dict["user_id"], ticket_dict["transaction_id"],ticket_dict['transaction_status'], ticket_dict['ticket_status'], ticket_dict["phone_num"], ticket_dict["museum"], 
                 ticket_dict["location"], ticket_dict["adult"], ticket_dict["child"], 
                 ticket_dict["date"], ticket_dict["adult_price"], ticket_dict["child_price"], ticket_dict["total_cost"]))


        # Step 5: Commit and close the connection
        conn.commit()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
    

def add_user(person):
    try:
        # Generate a unique user_id automatically
        user_id = str(uuid.uuid4())

        # Extract required fields from the `person` dictionary
        username = person["username"]
        nationality = person["nationality"]
        email = person["email"]
        phone = person["phone"]
        password = person["password"]
        dob = person["dob"]

        # Connect to the SQLite database
        conn = sqlite3.connect('database/user.db')
        cursor = conn.cursor()

        # Create the table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                        user_id TEXT PRIMARY KEY, 
                        username TEXT, 
                        nationality TEXT, 
                        email TEXT, 
                        phone TEXT, 
                        password TEXT, 
                        dob TEXT)''')

        # Insert user information into the table
        cursor.execute('''INSERT INTO user_info (user_id, username, nationality, email, phone, password, dob) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (user_id, username, nationality, email, phone, password, dob))

        # Commit and close the connection
        conn.commit()
        conn.close()

        print(f"User {username} added successfully with user_id: {user_id}")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False