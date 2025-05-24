# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod
#module required to create password hashes
import bcrypt
#module requiered for regular expressions
import re
from app.models.repositories.users import firebase_user_repository

repo = firebase_user_repository.FirebaseUserRepository()

class PasswordService(ABC):
    def __init__(self):
        pass
    
    #@abstractmethod
    def get_stored_hash_password(self, user):

        #The line belows must be the productive code. The DB must store a hash, right now it's storing the password in plain text
        #return user["password"]

        #we hash the password since it's currently stored in plain text in the DB
        return self.get_mock_hash_password(user["password"])

    #the new hash password must be store to the DB
    #@abstractmethod
    def store_new_pass_to_db(self, new_hash_password, user):
        return repo.update_user_password(user["email"], new_hash_password)

    #mock function to retrieve a password hash
    #only available while passwords are stored in plain text in the DB
    def get_mock_hash_password(self, hash_password: str):
        plain_text_pass = hash_password
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_text_pass.encode('utf-8'), salt)


    #8 caracteres, mayusculas, minusculas, números y simbolos
    def validate_password(self, new_pass_input: str) -> bool:
       
        valid_password = True

        # At last 8 characters
        if len(new_pass_input) < 8:
            valid_password = False

        # At least a lowercase letter
        if not re.search(r"[a-z]", new_pass_input):
            valid_password = False

        # At least an upercase letter
        if not re.search(r"[A-Z]", new_pass_input):
            valid_password = False

        # At least a number
        if not re.search(r"\d", new_pass_input):
            valid_password = False

        # At least a simbol
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\\/\[\]`~';]", new_pass_input):
            valid_password = False
        return valid_password

class ChangePasswordService(PasswordService):

    def verify_password(self, current_pass_input: str, mocked_hashed_pass):
        return bcrypt.checkpw(current_pass_input.encode('utf-8'), mocked_hashed_pass)


    def change_password(self, current_pass_input:str, new_pass_input:str, user):

        pass_change_successfully = False

        hashed_password = self.get_stored_hash_password(user)

        if (self.verify_password(current_pass_input, hashed_password)):
            salt = bcrypt.gensalt()
            new_hash_password = bcrypt.hashpw(new_pass_input.encode('utf-8'), salt)
            #self.store_new_pass_to_db(new_hash_password, user)  
            #we  don't pass the hash yet, since passwords are stored in plain text for the moment
            pass_change_successfully = self.store_new_pass_to_db(new_pass_input, user) 
        return pass_change_successfully
    
class ResetPasswordService(PasswordService):
    pass


class ForgotPasswordService(PasswordService):
    pass