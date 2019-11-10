from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Algorithms:
    loc=[]
    labels=['s1','s2','s4','s5','s6','s7','s8','s9','s10','s11','s12']
    def __init__(self, data):
        self.inlet=data['s1']
        self.outlet=data['s3']+data['s4']+data['s5']
        self.X=[]
        for index in labels:
            self.X.append(data[index])
    

    def checkleak(this):
        #inlet=data['s1']
        #outlet=data['s3']+data['s4']+data['s5']
        if abs(this.inlet-this.outlet) > threshold:
            return True
        return False

    def locateleak(self):
        from keras.models import load_model
        model=load_model('m.h5')
        y=model.predict_classes(self.X)
        return loc[y]