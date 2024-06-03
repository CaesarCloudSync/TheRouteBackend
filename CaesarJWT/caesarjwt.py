import jwt
import hashlib
from CaesarSQLDB.caesarcrud import CaesarCRUD
class CaesarJWT:
    def __init__(self,caesarcrud : CaesarCRUD) -> None:
        self.caesarcrud = caesarcrud
        self.JWT_SECRET = "Peter Piper picked a peck of pickled peppers, A peck of pickled peppers Peter Piper picked, If Peter Piper picked a peck of pickled peppers,Where's the peck of pickled peppers Peter Piper picked" #'super-secret'
        # IRL we should NEVER hardcode the secret: it should be an evironment variable!!!
        self.JWT_ALGORITHM = "HS256"
    def secure_encode(self,token):
        # if we want to sign/encrypt the JSON object: {"hello": "world"}, we can do it as follows
        # encoded = jwt.encode({"hello": "world"}, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        encoded_token = jwt.encode(token, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        # this is often used on the client side to encode the user's email address or other properties
        return encoded_token

    def secure_decode(self,token):
        # if we want to sign/encrypt the JSON object: {"hello": "world"}, we can do it as follows
        # encoded = jwt.encode({"hello": "world"}, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        decoded_token = jwt.decode(token, self.JWT_SECRET, algorithms=self.JWT_ALGORITHM)
        # this is often used on the client side to encode the user's email address or other properties
        return decoded_token
    def provide_access_token(self,login_details,student=0):
        condition = f"email = '{login_details['email']}'"
        if student == 0:
            email_exists = self.caesarcrud.check_exists(("*"),"users",condition=condition)
        elif student == 1:
            email_exists = self.caesarcrud.check_exists(("*"),"studentsubscriptions",condition=condition)
        if email_exists:
            encrypted_password =  hashlib.sha256(login_details["password"].encode('utf-8')).hexdigest()
            email_data = self.caesarcrud.get_data(("email","password"),"users",condition=condition)[0]
            if email_data["password"] == encrypted_password:
                access_token = self.secure_encode({"email":email_data["email"]}) #create_access_token(identity=email_exists["email"])
                return access_token
            else:
                return "Wrong password"
        else:
            return "Wrong password"