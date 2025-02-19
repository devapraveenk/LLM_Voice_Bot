def transform_json(data):
    # Extract relevant information from the input data
    museum = data['museum']
    location = data['location']
    adult_count = data['tickets']['adult']
    child_count = data['tickets']['child']
    date = data['date']
    adult_price = data['price']['adult']
    total_cost = data['total_cost']

    # Calculate child price based on adult price (assuming a fixed ratio)
    child_price = 20  # Adjust this as needed

    # Create the transformed JSON data
    transformed_data = {
        "museum": museum,
        "location": location,
        "adult": adult_count,
        "child": child_count,
        "date": date,
        "adult_price": adult_price,
        "child_price": child_price,
        "total_cost": total_cost
    }

    return transformed_data


data = {
  "order_amount": {
    "museum": "Rabindra Bharati Museum",
    "location": "Kolkata",
    "tickets": {
      "adult": 1,
      "child": 0
    },
    "date": "next week",
    "price": {
      "adult": 50
    },
    "total_cost": 50
  }
}

res = transform_json(data['order_amount'])
print(res)