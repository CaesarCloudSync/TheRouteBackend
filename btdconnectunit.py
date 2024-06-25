import json
import requests
import unittest
import sys
import time
from UnittestData.QualificationsData import QualificationsInfo

uri = "http://127.0.0.1:8080" #"https://btdtechconnectbe-hrjw5cc7pa-uc.a.run.app"
def create_qualification(qualification,qual_info):
    response = requests.post(f"{uri}/api/v1/storecareerentity",json={"career":qualification["career"],"label":qualification["career"].replace("_"," ",100).title(),"industry":qualification["industry"]})
    print(response.json())
    response = requests.post(f"{uri}/api/v1/storeinstitution",json={"institution":qualification["institution"]})
    print(response.json())
    qualification["description"] = qual_info.qual_description
    response = requests.post(f"{uri}/api/v1/storequalification",json=qualification)
    print(response.json())
    
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
        response = requests.post(f"{uri}/api/v1/storeindustryentity",json={"industry":"finance","label":"Finance"})

        response = requests.post(f"{uri}/api/v1/storecareerentity",json={"career":"accountant","label":"Accountant","industry":"finance"})
        

        print(response.json())
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
        "qual_icon": "https://www.blast.co.uk/wp-content/uploads/blast_design_croydoncollege_Identity_print_2a.jpg",
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
        "qual_image":"https://feweek.co.uk/wp-content/uploads/2016/11/p5-Croydon-College.jpg"
    })
        print(response.json())

        response = requests.post(f"{uri}/api/v1/storequalification",json={
                "qual_name": "Game Designer",
                "industry":"gaming",
                "career":"game_designer",
                "link": "https://www.universitygames.com/",
                "description":qual_info.qual_description,
                "qual_icon": "https://cdn.vox-cdn.com/thumbor/JPRYCY0yKtFT9ccqUcVoeiXvwTk=/150x0:1770x1080/920x613/filters:focal(150x0:1770x1080):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/45700578/twitch.0.0.jpg",
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
        response = requests.post(f"{uri}/api/v1/storeinstitution",json={"institution":"LSE University"})
        

        print(response.json())
        response = requests.post(f"{uri}/api/v1/storequalification",json={
        "qual_name": "BSE Economics",
        "industry":"finance",
        "career":"accountant",
        "link": "https://www.lse.ac.uk/",
        "description":qual_info.qual_description,
        "qual_icon": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/LSE_Logo.svg/319px-LSE_Logo.svg.png?20110331145302",
        "institution": "LSE University",
        "online_freq": "1_days_a_week",
        "online_freq_label": "1 days a week",
        "in_person_freq": "4_day_a week",
        "in_person_freq_label": "4 day a week",
        "course_length": "4_years",
        "course_length_label": "4 Years Study",
        "earning_potential_lower": "90k",
        "earning_potential_upper": "140K",
        "earning_potential_description": "no experience needed",
        "qual_image":"https://www.goodenough.ac.uk/wp-content/uploads/2021/03/london-school-of-economics-glance-1.jpg"
    })
        
        response = requests.post(f"{uri}/api/v1/storeinstitution",json={"institution":"Oxford University"})
        

        print(response.json())
        response = requests.post(f"{uri}/api/v1/storequalification",json={
        "qual_name": "AI BSC Degree",
        "industry":"tech",
        "career":"software_developer",
        "link": "https://www.ox.ac.uk/",
        "description":qual_info.qual_description,
        "qual_icon": "https://i0.wp.com/oxforduniversitytours.co.uk/wp-content/uploads/2023/09/university-of-oxford-logo-1.png?resize=300%2C300&ssl=1",
        "institution": "Oxford University",
        "online_freq": "1_days_a_week",
        "online_freq_label": "1 days a week",
        "in_person_freq": "4_day_a week",
        "in_person_freq_label": "4 day a week",
        "course_length": "4_years",
        "course_length_label": "4 Years Study",
        "earning_potential_lower": "150k",
        "earning_potential_upper": "200K",
        "earning_potential_description": "no experience needed",
        "qual_image":"https://cdn.britannica.com/03/117103-050-F4C2FC83/view-University-of-Oxford-England-Oxfordshire.jpg?w=400&h=300&c=crop"
    })
        print(response.json())
        #response = requests.get(f"{uri}/api/v1/getqualifications?page=1")
        #print(response.json())
        #response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"amari.lawal@gmail.com","password":"test"})
        #print(response.json())
        #access_token = response.json()["access_token"]
        #headers = {"Authorization": f"Bearer {access_token}"}
        #response = requests.get(f"{uri}/api/v1/getuserinterests",headers=headers)
        #print(response.json())
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"amari.lawal@gmail.com","password":"test"})
        print(response.json())
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        #response = requests.get(f"{uri}/api/v1/getbookmarkedqualifications",headers=headers)
        #print(response.json())
        response = requests.get(f"{uri}/api/v1/getuserinterestqualifications",params={"offset":8},headers=headers)
        print(response.json())
        #with open("UnittestData/Qualifications.json") as f:
        #    qualifications = json.load(f)
        #for qual in qualifications:
        #    create_qualification(qual,qual_info)
        #    time.sleep(1)
    def test_search(self):
        response = requests.get(f"{uri}/api/v1/searchqualifications",params={"offset":1,"text":"Ox"})
        print(response.json())
    def test_delete_user(self):
        response = requests.post(f"{uri}/api/v1/loginapi",json={"email":"amari.lawal@gmail.com","password":"test"})
        print(response.json())
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(f"{uri}/api/v1/deleteuser",headers=headers)
        print(response.json())
    def test_create_account(self):
        signup_json = {"date_of_birth": "2024-06-25", "email": "amari.lawal@gmail.com", "first_name": "Amari", "last_name": "Lawal", "password": "test"}
        interetsts_json = {"career": "software_developer", "industry": "tech", "studydays": "3_days_week", "studypref": "online"}
        response = requests.post(f"{uri}/api/v1/signupapi",json=signup_json)
        print(response.json())
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post("http://172.20.10.3:8080/api/v1/storeuserinterests",json=interetsts_json,headers=headers)
        print(response.json())


if __name__ == "__main__":
    unittest.main()