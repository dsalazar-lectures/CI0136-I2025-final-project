# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod
import bcrypt

class PasswordService(ABC):
    def __init__(self):
        pass
    
    #@abstractmethod
    def get_stored_hash_password(user):
        pass

    #the new hash password must be store to the DB
    #@abstractmethod
    def store_new_pass_to_db(self, new_hash_password, user):
        pass

    #mock function to retrieve a temp hash password
    #only available while the DB doesn't exist
    def get_mock_hash_password(self):
        plain_text_pass = "contraseña"
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_text_pass.encode('utf-8'), salt)


class ChangePasswordService(PasswordService):

    def verify_password(self, current_pass_input: str, mocked_hashed_pass):
        return bcrypt.checkpw(current_pass_input.encode('utf-8'), mocked_hashed_pass)


    def change_password(self, current_pass_input:str, new_pass_input:str, user):
        #the hash password must be retreived from the DB
        pass_change_successfully = False

        #temporal, it must be change for get_stored_hash_password() whenever the DB is available
        mocked_hashed_pass = self.get_mock_hash_password() 

        if (self.verify_password(current_pass_input, mocked_hashed_pass)):
            salt = bcrypt.gensalt()
            new_hash_password = bcrypt.hashpw(new_pass_input.encode('utf-8'), salt)
            self.store_new_pass_to_db(new_hash_password, user)  
            pass_change_successfully = True
        return pass_change_successfully
    
class ResetPasswordService(PasswordService):
    pass


class ForgotPasswordService(PasswordService):
    pass