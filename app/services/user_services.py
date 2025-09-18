from app import db
from app.models.mycontact import Users
from werkzeug.security import generate_password_hash, check_password_hash

class UserServices:
    def __init__(self):
        self.Users = Users
        self.db = db
    
    def register(self, username, password):
        try:
            hash_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
            new_user = self.Users(username=username, password=hash_password)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        except Exception as e:
            self.db.session.rollback()
            return {"error": str(e)}
        
    def login(self, username, password):
        try:
            user = self.Users.query.filter_by(username=username).first()
            if not user:
                return None
            
            if check_password_hash(user.password, password):
                return user
            else:
                return None
        except Exception as e:
            return {"error": str(e)}
    

