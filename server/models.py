from server.custom_validations import ValidationError
from server.scripts import make_password , generate_random_password

class ChatUser:
    def __init__(self,client):
        self.client = client
        self.password = None
        self.role = None

        
    
    def change_password(self,old_password,new_passwod,new_password_2):
        if new_passwod != new_password_2:
            raise ValidationError("passwords does not match!")
        if old_password != self.password:
            raise ValidationError("sth is wrong")
        
        self.password = make_password(new_passwod)
    
    def set_random_password(self):
        _ , random_password = generate_random_password()
        self.password = random_password
    
    
    def set_password(self,password):
        self.password = make_password(password)
        
        
        
        
        
        
        


        