import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import date, timedelta
import requests
import oracledb
from sqlalchemy.pool import NullPool
from models import User, Stock, db

app = Flask(__name__)
CORS(app)

#db = SQLAlchemy()

#Environment
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

#Database Configuration
un = 'ADMIN'
pw = 'Capstone27!!'
dsn = '''(description=(retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.eu-madrid-1.oraclecloud.com))(connect_data=(service_name=g12f280add2aa88_capstonemiranda_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''

pool = oracledb.create_pool(user=un,password=pw,dsn=dsn)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+oracledb://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'creator': pool.acquire,
    'poolclass': NullPool
}
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

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
    
    last_available_date = sorted(time_series.keys(), reverse=True)[0]
    closing_value = time_series[last_available_date].get("4. close")
    return closing_value if closing_value else "Data not available"


#Fetch stock data from Alpha Vantage API
def fetch_stock_data(symbol, start_date=None, end_date=None):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

#Filter stock data to return the specified number of days
def filter_stock_data(data, days):
    series = data['Time Series (Daily)']
    start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = date.today().strftime("%Y-%m-%d")
    return {date: details for date, details in series.items() if start_date <= date <= end_date}


#Milestone 0 Requirement: When any of the symbols is selected, then its current and relevant past values appear on screen
@app.route("/api/portfolio/<SYMBOL>", methods=['GET'])
def stock_history(SYMBOL):
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    data = fetch_stock_data(SYMBOL, start_date=start_date, end_date=end_date)

    #Error handling - Handle the case where the API call failed due to network issues or Alpha Vantage API problems
    if data is None:
        return jsonify({"error": "Failed to fetch stock data, please try again later."}), 500

    if 'Note' in data:
        #Error handling - Specific message for API limit reached
        return jsonify({"error": "API request limit reached. Please wait and try again later."}), 429
    
    if 'Error Message' in data:
        #Error handling -  Specific message for invalid symbol
        return jsonify({"error": "The stock symbol doesn't exist. Please check the symbol and try again."}), 400

    if 'Time Series (Daily)' in data:
        time_series = data['Time Series (Daily)']
        
        if start_date and end_date:
            filtered_series = {date: details for date, details in time_series.items() if start_date <= date <= end_date}
            
            if not filtered_series:
                return jsonify({"error": "We don't have stock data for the dates entered. Please try different dates."}), 404
            
            return jsonify(filtered_series)
        else:
            return jsonify(time_series)
    else:
        return jsonify({"error": "Stock data not found. Please check your request and try again."}), 404


#Milestone 1 Requirement: Total Portfolio Value + stocks in portfolio 
@app.route("/api/portfolio", methods=['GET'])
def portfolio_value():
    user_id = request.args.get('user_id') 
    if user_id is not None:
        user_id = int(user_id)  
    else:
        return jsonify({"error": "No user_id provided"}), 400

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    total_value = 0
    stocks_detail = []
    for stock in user.portfolio:
        current_price = float(fetch_last_closing_value(stock.symbol))
        stock_value = current_price * stock.quantity
        total_value += stock_value
        stocks_detail.append({
            "symbol": stock.symbol,
            "quantity": stock.quantity,
            "current_price": current_price,
            "stock_value": stock_value
        })

    return jsonify({
        "total_portfolio_value": total_value,
        "stocks": stocks_detail
    })

#New: Milestone 2 Requirement: Modify portfolio 
@app.route("/update_user", methods=['PUT'])
def update_user_portfolio():
    data = request.get_json()
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    for add in data.get('add', []):  
        symbol = add.get('symbol').upper()
        quantity = add.get('quantity')
        
        existing_stock = Stock.query.filter_by(user_id=user_id, symbol=symbol).first()
        if existing_stock:
            existing_stock.quantity += quantity
        else:
            new_stock = Stock(symbol=symbol, quantity=quantity, user_id=user_id)
            db.session.add(new_stock)

    for remove in data.get('remove', []):  
        symbol = remove.get('symbol').upper()
        quantity = remove.get('quantity')
        
        existing_stock = Stock.query.filter_by(user_id=user_id, symbol=symbol).first()
        if existing_stock:
            if existing_stock.quantity > quantity:
                existing_stock.quantity -= quantity
            elif existing_stock.quantity == quantity:
                db.session.delete(existing_stock)
            else:
                return jsonify({"error": f"Not enough shares of {symbol} to remove"}), 400
        else:
            return jsonify({"error": f"Stock {symbol} not found in portfolio"}), 404

    db.session.commit()
    return jsonify({"message": "Portfolio updated successfully"})

#This fetches the username for the mainpage frontend to identify the user logged in (for the 'Welcome, user!')
@app.route("/user-details", methods=['GET'])
def user_details():
    user_id = request.args.get('user_id')  
    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "username": user.username
    })

if __name__ == "__main__":
    app.run(debug=True)


