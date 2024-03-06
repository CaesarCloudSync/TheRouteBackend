import json
import requests
import unittest
import sys

uri = "http://127.0.0.1:8080" #"https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app"

class BTDConnectUnittest(unittest.TestCase):
    def test_signup(self):
        response = requests.post(f"{uri}/api/v1/signupapi",json={"email":"test@example.com","password":"test"})
        print(response.json())
    def test_login(self):
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"test@example.com","password":"test"})
        print(response.json())
    def test_get_info(self):
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"test@example.com","password":"test"})
        print(response.json())
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{uri}/api/v1/getuserinfo",headers=headers)
        print(response.json())




if __name__ == "__main__":
    unittest.main()