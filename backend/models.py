from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Identity

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  
    user_id = db.Column(db.Integer,Identity(start=1, cycle=False), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    portfolio = db.relationship('Stock', backref='user', lazy=True)
   
    def to_json(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'portfolio': [stock.to_json() for stock in self.portfolio]
        }

class Stock(db.Model):
    __tablename__ = 'stocks'
    stock_id = db.Column(db.Integer, Identity(start=1, cycle=False), primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
   
    def to_json(self):
        return {
            'stock_id': self.stock_id,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'user_id': self.user_id
        }
