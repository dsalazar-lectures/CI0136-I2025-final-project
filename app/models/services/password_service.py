# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod
#module required to create password hashes
import bcrypt
#module requiered for regular expressions
import re
from app.models.repositories.users import firebase_user_repository
from flask import session

class PasswordService(ABC):
    def __init__(self):
        pass
    
    #@abstractmethod
    def get_stored_hash_password(self, user):
        repo = firebase_user_repository.FirebaseUserRepository()
        user = repo.get_user_by_id(user)

        #The line belows must be the productive code. The DB must store a hash, right now it's in plain text
        #return user["password"]

        #we hash the password since it's in plain text in the DB for the moment
        return self.get_mock_hash_password(user["password"])

    #the new hash password must be store to the DB
    #@abstractmethod
    def store_new_pass_to_db(self, new_hash_password, user):
        pass

    #mock function to retrieve a temp hash password
    #only available while the DB doesn't exist
    def get_mock_hash_password(self, hash_password: str):
        #plain_text_pass = "contraseña"
        plain_text_pass = hash_password
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_text_pass.encode('utf-8'), salt)

    #Passtraseña123.
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
        #the hash password must be retreived from the DB
        pass_change_successfully = False

        #temporal, it must be change for get_stored_hash_password() whenever the DB is available
        #mocked_hashed_pass = self.get_mock_hash_password("contraseña") 

        mocked_hashed_pass = self.get_stored_hash_password(session["user_id"])

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