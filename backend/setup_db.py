from app import app, db  # Make sure this import matches how you've structured your app and db
from models import User, Stock
from datetime import datetime

def setup_users_and_stocks():
    # Define the users and their stocks
    users_data = [
        {"username": "User1", "stocks": [("AAPL", 10, "2023-01-01"), ("GOOG", 5, "2023-02-01")]},
        {"username": "User2", "stocks": [("MSFT", 15, "2023-01-15"), ("AMZN", 4, "2023-02-15")]},
        {"username": "User3", "stocks": [("TSLA", 8, "2023-03-01"), ("NFLX", 10, "2023-03-15")]}
    ]

    # Iterate over the users data to create User and Stock objects
    for user_data in users_data:
        user = User(username=user_data["username"])
        db.session.add(user)
        db.session.commit()  # Commit to assign an ID to the user

        for symbol, quantity, purchase_date in user_data["stocks"]:
            stock = Stock(symbol=symbol, quantity=quantity, purchase_date=datetime.strptime(purchase_date, "%Y-%m-%d"), user_id=user.id)
            db.session.add(stock)

    # Commit the stocks to the database
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():  # This line is the key to running within the Flask application context
        setup_users_and_stocks()
        print("Users and stocks setup complete.")
