import json
import requests
import unittest
import sys
from UnittestData.QualificationsData import QualificationsInfo

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
        response = requests.post(f"{uri}/api/v1/storeinstitution",json={"institution":"Croydon College"})
        

        print(response.json())
        response = requests.post(f"{uri}/api/v1/storeinstitution",json={"institution":"GAMES ARE US"})
        

        print(response.json())
        response = requests.post(f"{uri}/api/v1/storecareerentity",json={"career":"game_designer","label":"Game Designer","industry":"gaming"})
        

        print(response.json())
        qual_info = QualificationsInfo()
        response = requests.post(f"{uri}/api/v1/storequalification",json={
        "qual_name": "Game Development",
        "industry":"gaming",
        "career":"game_developer",
        "link": "https://croydon.ac.uk/",
        "description":qual_info.qual_description,
        "qual_icon": "https://qual_icon",
        "institution": "Croydon College",
        "online_freq": "2_days_a_week",
        "online_freq_label": "2 days a week",
        "in_person_freq": "1_day_a week",
        "in_person_freq_label": "1 day a week",
        "course_length": "2_years",
        "course_length_label": "2 Years Study",
        "earning_potential_lower": "60k",
        "earning_potential_upper": "180K",
        "earning_potential_description": "no experience needed",
        "qual_image":"https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/home-improvement/wp-content/uploads/2022/07/Paris_Exterior_4-Edit-e1714649473120.png"
    })
        print(response.json())
        response = requests.post(f"{uri}/api/v1/storequalification",json={
                "qual_name": "Game Designer",
                "industry":"gaming",
                "career":"game_designer",
                "link": "https://www.universitygames.com/",
                "description":qual_info.qual_description,
                "qual_icon": "https://qual_icon",
                "institution": "GAMES ARE US",
                "online_freq": "4_days_a_week",
                "online_freq_label": "4 days a week",
                "in_person_freq": "",
                "in_person_freq_label":"",
                "course_length": "18_months", 
                "course_length_label":"18 Months Study",
                "earning_potential_lower": "75k",
                "earning_potential_upper": "120K",
                "earning_potential_description": "3 months training provided before job offer",
                "qual_image":"https://jkeducate.b-cdn.net/content/uploads/2024/05/classroom-2093744_1920.jpg"
            })
        print(response.json())
        response = requests.get(f"{uri}/api/v1/getqualifications?page=1")
        #print(response.json())
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"amari.lawal@gmail.com","password":"test"})
        #print(response.json())
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{uri}/api/v1/getuserinterests",headers=headers)
        print(response.json())



if __name__ == "__main__":
    unittest.main()