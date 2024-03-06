import hashlib
import uuid

class CaesarHash:
    @staticmethod
    def hash_text_auth(text):
        """
            Basic hashing function for a text using random unique salt.  
        """
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt
    @staticmethod
    def hash_text(text):
        """
            Basic hashing function for a text.
        """
        return hashlib.sha256(text.encode()).hexdigest() 
    @staticmethod
    def match_hashed_text(hashedText, providedText):
        """
            Check for the text in the hashed text
        """
        _hashedText, salt = hashedText.split(':')
        return _hashedText == hashlib.sha256(salt.encode() + providedText.encode()).hexdigest()
    @staticmethod
    def hash_quota(data:dict):
        hashinput = data["quotatitle"].lower().replace(" ","",100) + data["quotatype"].lower().replace(" ","",100)
        quotahash = CaesarHash.hash_text(hashinput)
        return quotahash
