import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import date, timedelta

app = Flask(__name__)

#Database Configuration with Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_stocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

from models import User, Stock

def calculate_previous_weekday():
    today = date.today()
    offset = (today.weekday() - 1) % 7 
    last_weekday = today - timedelta(days=offset)
    return last_weekday

#Fetch the last closing value for a given stock symbol
def fetch_last_closing_value(stock):
    data = fetch_stock_data(stock)
    time_series = data.get("Time Series (Daily)", {})
    if not time_series:
        return "Data not available"
    
    # Sort the dates and get the most recent one
    last_available_date = sorted(time_series.keys(), reverse=True)[0]
    closing_value = time_series[last_available_date].get("4. close")
    return closing_value if closing_value else "Data not available"


#Fetch stock data from Alpha Vantage API
def fetch_stock_data(stock, start_date=None, end_date=None):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}&outputsize=full"
    response = requests.get(url)
    data = response.json()
    return data

#Filter stock data to return the specified number of days
def filter_stock_data(data, days):
    series = data['Time Series (Daily)']
    start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = date.today().strftime("%Y-%m-%d")
    return {date: details for date, details in series.items() if start_date <= date <= end_date}

#Milestone 0 Requirement: The app displays a list with all the symbols belonging to the portfolio.
#This wasn't working before but now its working well
@app.route("/api/portfolio", methods=['GET'])
def portfolio():
    user_id = request.args.get('userId')
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    portfolio = {stock.symbol: stock.quantity for stock in user.portfolio}
    return jsonify({"stocks": portfolio})

#Milestone 0 Requirement: When any of the symbols is selected, then its current and relevant past values appear on screen
#This was working before but I had to make changes when I implemented the new db because of the formatting of the dates
@app.route("/api/stock/<symbol>", methods=['GET'])
def stock_history(symbol):
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    data = fetch_stock_data(symbol, start_date=start_date, end_date=end_date)

    if 'Time Series (Daily)' in data:
        time_series = data['Time Series (Daily)']
        
        if start_date and end_date:
            filtered_series = {date: details for date, details in time_series.items() if start_date <= date <= end_date}
            return jsonify(filtered_series)
        else:
            return jsonify(time_series)
    else:
        return jsonify({"error": "Stock data not found or API limit reached"}), 404

#New: Milestone 1 Requirement: Total Portfolio Value 
@app.route("/api/portfolio/value", methods=['GET'])
def portfolio_value():
    user_id = request.args.get('userId')
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    total_value = 0
    for stock in user.portfolio:
        current_price = float(fetch_last_closing_value(stock.symbol))
        total_value += current_price * stock.quantity

    return jsonify({"total_portfolio_value": total_value})

#Initialize DB before the first request is processed
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


