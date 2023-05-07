from datetime import datetime
##to irradicate circular import error
# from __main__ import db
from SearchWebsite import db, loginmanager
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique =True, nullable = False)
    email = db.Column(db.String(120), unique =True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    searches = db.relationship('pquery', backref = 'author', lazy =True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class pquery(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    #query
    q = db.Column(db.String(120), nullable = False)
    date_searched = db.Column(db.DateTime, nullable = False,  default = datetime.utcnow())
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)
    def __repr__(self):
        return self.q