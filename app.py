import json
import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import date, timedelta

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

#Utility functions
def read_user_database():
    with open("user_database.json", 'r') as db_file:
        return json.load(db_file)

#Retrieve the stock list for a given user ID
def find_user_stocks(user_id):
    db = read_user_database()
    return db.get(user_id, "User not found in database.")

#Calculate the last weekday date
def calculate_previous_weekday():
    today = date.today()
    offset = 1 if today.weekday() >= 1 else 3 if today.weekday() == 0 else 2
    last_weekday = today - timedelta(days=offset)
    return last_weekday.strftime("%Y-%m-%d")

#API endpoints
@app.route("/api/portfolio", methods=['GET'])
def portfolio():
    user_id = request.args.get('userId', 'user1')  #Get user ID from request
    stocks = find_user_stocks(user_id)
    if isinstance(stocks, str):  
        return jsonify({"error": stocks}), 404
    stock_values = {stock: fetch_last_closing_value(stock) for stock in stocks}
    return jsonify(stock_values)

@app.route("/api/portfolio/<stock>", methods=['GET'])
def stock_value(stock):
    data = fetch_stock_data(stock, days=30)  # Get data for the last 30 days
    return jsonify({
        "symbol": stock,
        "values_daily": data
    })

#Fetch the last closing value for a given stock symbol
def fetch_last_closing_value(stock):
    data = fetch_stock_data(stock)
    last_weekday = calculate_previous_weekday()
    return data["Time Series (Daily)"][last_weekday]["4. close"]

#Fetch stock data from Alpha Vantage API
def fetch_stock_data(stock, days=1):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if days > 1:
        return filter_stock_data(data, days)
    return data

#Filter stock data to return the specified number of days
def filter_stock_data(data, days):
    series = data['Time Series (Daily)']
    start_date = (date.today()-timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = date.today().strftime("%Y-%m-%d")
    return {date: details for date, details in series.items() if start_date <= date <= end_date}

if __name__ == "__main__":
    app.run(debug=True)
