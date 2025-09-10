from app import db

class MyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20))
    email = db.Column(db.String(30))


    def __repr__(self):
        return f"<Phone_number = {self.phone_number}>"
    