from miniagent import db

class Account(db.Model):
   id = db.Column(db.Integer, primary_key = True, nullable=False)
   event_id = db.Column(db.String(100), nullable=False)
   account_id = db.Column(db.String(100), nullable=False)
   user_name = db.Column(db.String(100), nullable=False)
   created_date = db.Column(db.DateTime())