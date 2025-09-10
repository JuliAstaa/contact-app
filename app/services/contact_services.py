from app import db
from app.models.mycontact import MyContact 


class ContactServices:
    def __init__(self):
        self.MyContact = MyContact
        self.db = db
        
    def create_contact(self, phone_number: str, f_name:str, l_name:str, email:str):
        try:
            new_contact = self.MyContact(phone_number=phone_number, f_name=f_name, l_name=l_name, email=email)
            self.db.session.add(new_contact)
            self.db.session.commit()
            return new_contact
        except:
            db.session.rollback()
            return False
    
    def get_all_contact(self):
        return self.MyContact.query.all()
    
    def get_data_by_id(self, id:int):
        try:
            user_by_id = self.MyContact.query.get_or_404(id)
            return user_by_id
        except:
            return "User Not Found"
    
    def edit_contact(self, user, phone_number: str, f_name:str, l_name:str, email:str):
        user.phone_number = phone_number
        user.f_name = f_name
        user.l_name = l_name
        user.email = email

        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
        
    def remove_contact(self, user):
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    
    
        