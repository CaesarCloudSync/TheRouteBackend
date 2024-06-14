import json
import requests
import unittest
import sys

uri = "http://127.0.0.1:8080" #"https://btdtechconnectbe-hrjw5cc7pa-uc.a.run.app"

class BTDConnectUnittest(unittest.TestCase):
    def test_signup(self):
        response = requests.post(f"{uri}/api/v1/signupapi",json={"first_name":"Amari","last_name":"Lawal","email":"amari.lawal@gmail.com","password":"test","date_of_birth":"2024-06-03"})

        print(response.json())
    def test_login(self):
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"amari.lawal@gmail.com","password":"test"})
        print(response.json())
    def test_get_info(self):
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"test@example.com","password":"test"})
        print(response.json())
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{uri}/api/v1/getuserinfo",headers=headers)
        print(response.json())
    def test_store_industry_intersts(self):
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"amari.lawal@gmail.com","password":"test"})
        print(response.json())
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{uri}/api/v1/storeuserinterests",json={"industry":"tech","career":"software_developer","studypref":"online","studydays":"3_days_week"},headers=headers)
        print(response.json())
    def test_get_industry_choices(self):
        response = requests.get(f"{uri}/api/v1/getindustrychoices")
        print(response.json())
    def test_insert_industrys_careers_studydays_studyprefs(self):
        response = requests.post(f"{uri}/api/v1/storeindustryentity",json={"industry":"tech","label":"Technology"})
        response = requests.post(f"{uri}/api/v1/storeindustryentity",json={"industry":"gaming","label":"Gaming"})


        print(response.json())
        response = requests.post(f"{uri}/api/v1/storecareerentity",json={"career":"software_developer","label":"Software Developer","industry":"tech"})
        

        print(response.json())
        response = requests.post(f"{uri}/api/v1/storecareerentity",json={"career":"software_designer","label":"Software Designer","industry":"tech"})
        

        print(response.json())
        response = requests.post(f"{uri}/api/v1/storecareerentity",json={"career":"game_developer","label":"Game Developer","industry":"gaming"})
        

        print(response.json())
        #{"industry":"tech","career":"software_developer","studypref":"online","studydays":"3"}

        response = requests.post(f"{uri}/api/v1/storestudyprefentity",json={"studypref":"online","label":"Online"})
        

        print(response.json())

        response = requests.post(f"{uri}/api/v1/storestudydayentity",json={"studydays":"3_days_week","label":"3 Days a week"})
        

        print(response.json())



if __name__ == "__main__":
    unittest.main()