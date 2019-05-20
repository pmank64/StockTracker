from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Symbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(60), index=True)
    company_name = db.Column(db.String(120), index=True)
    # current_price = db.Column(db.Float)
    sentiment_score = db.Column(db.Float)
    # pe_ratio = db.Column(db.Float)
    # msr = db.Column(db.Float)
