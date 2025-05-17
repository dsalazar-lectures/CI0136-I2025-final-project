# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod
import bcrypt

class password_service():
    def __init__(self):
        pass
    
    #mock function to retrieve a temp hash password
    def get_mock_hash_password(self):
        plain_text_pass = "contraseña"
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_text_pass.encode('utf-8'), salt)
    
    #the new hash password must be store to the DB
    def store_new_pass_to_db(self, new_hash_password):
        pass

    def verify_password(self, current_pass_input: str, mocked_hashed_pass):
        return bcrypt.checkpw(current_pass_input.encode('utf-8'), mocked_hashed_pass)


    def change_password(self, current_pass_input:str, new_pass_input:str):
        #the hash password must be retreived from the DB
        pass_change_successfully = False
        mocked_hashed_pass = self.get_mock_hash_password() #temporal
        if (self.verify_password(current_pass_input, mocked_hashed_pass)):
            salt = bcrypt.gensalt()
            new_hash_password = bcrypt.hashpw(new_pass_input.encode('utf-8'), salt)
            self.store_new_pass_to_db(new_hash_password)
            pass_change_successfully = True
        return pass_change_successfully