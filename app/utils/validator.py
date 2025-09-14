import re
from app.models.mycontact import MyContact

class Validator:
    @staticmethod    
    def is_empty(s: str):
        if not s:
            return True
        else:
            return False

    @staticmethod  
    def valid_name(s: str):
        if not re.match(r"^[A-Za-z.' ]+$", s):
            return True
        else:
            return False

    @staticmethod
    def valid_phone_number(phone_number: str):
        if not phone_number.isdigit():
            return True
        else:
            return False
    
    @staticmethod
    def valid_email(email: str):
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            return True
        else:
            return False
    
class FormValidator(Validator):
    def __init__(self, phone_number, f_name, l_name, email, id=None):
        self.phone_number = phone_number
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.id = id
        self.errors = {}
    
    def add_error(self, key, value):
        if key not in self.errors:
            self.errors[key] = []
        
        self.errors[key].append(value)

    def validate_fname(self):
        if self.is_empty(self.f_name):
            self.add_error('f_name', "First name can't be empty!")
            pass
        
        if self.valid_name(self.f_name):
            self.add_error('f_name', "Name is not Valid")
            pass

    def validate_lname(self):
        if self.valid_name(self.l_name):
            self.add_error('l_name', "Name is not Valid")
            pass
    
    def validate_phone_number(self):
        if self.is_empty(self.phone_number):
            self.add_error('phone_number', "Phone number can't be empty!")
            pass
        
        if self.valid_phone_number(self.phone_number):
            self.add_error('phone_number', f"Phone number is not Valid")
            pass

        # cek duplikasi
        is_email_taken = MyContact.query.filter_by(email = self.email).first()
        if is_email_taken and is_email_taken.id != self.id:
            self.add_error('phone_number', "Phone number already taken")
            pass
    
    def validate_email(self):
        if self.valid_email(self.email):
            self.add_error('email', "Email is not Valid")
            pass
    

    def validate_all(self):
        self.validate_fname()
        self.validate_lname()
        self.validate_phone_number()
        self.validate_email()
        return self.errors