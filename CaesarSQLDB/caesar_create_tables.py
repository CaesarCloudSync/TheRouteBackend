from CaesarSQLDB.caesarcrud import CaesarCRUD
from psycopg import ProgrammingError
import uuid
class CaesarCreateTables:
    def __init__(self) -> None:
        self.qualifications_columns = ("qual_uuid","qual_name","industry","career",
                    "link",
                    "description",
                    "qual_icon",
                    "institution",
                    "online_freq",
                    "online_freq_label",
                    "in_person_freq",
                    "in_person_freq_label",            
                    "course_length",
                    "course_length_label",
                    "earning_potential_lower",
                    "earning_potential_upper",
                    "earning_potential_description",
                    "qual_image")
    def create(self,caesarcrud :CaesarCRUD):
        try:
            caesarcrud.caesarsql.run_command("""
            CREATE TABLE IF NOT EXISTS users (
                uuid UUID NOT NULL PRIMARY KEY, 
                email VARCHAR(255) NOT NULL,
                password TEXT NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                date_of_birth DATE NOT NULL
                );
            CREATE TABLE IF NOT EXISTS industrys (
                industry_uuid UUID NOT NULL PRIMARY KEY, 
                industry VARCHAR(255) NOT NULL,
                label VARCHAR(255) NOT NULL,
                CONSTRAINT order_date_unique UNIQUE (industry)
                );
            CREATE TABLE IF NOT EXISTS careers (
                career_uuid UUID NOT NULL PRIMARY KEY, 
                career VARCHAR(255) NOT NULL,
                label VARCHAR(255) NOT NULL,
                industry VARCHAR(255) REFERENCES industrys(industry) NOT NULL,
                career VARCHAR(255) REFERENCES careers(career) NOT NULL
                );
            CREATE TABLE IF NOT EXISTS studypreferences (
                studypref_uuid UUID NOT NULL PRIMARY KEY, 
                studypref VARCHAR(255) NOT NULL,
                label VARCHAR(255) NOT NULL
                );
            CREATE TABLE IF NOT EXISTS studydays (
                studyday_uuid UUID NOT NULL PRIMARY KEY, 
                studyday VARCHAR(255) NOT NULL,
                label VARCHAR(255) NOT NULL                             
                );
                                             
            CREATE TABLE IF NOT EXISTS users_interests (
                users_interests_uuid UUID NOT NULL PRIMARY KEY, 
                uuid UUID REFERENCES users(uuid) NOT NULL,
                industry_uuid UUID REFERENCES industrys(industry_uuid) NOT NULL,
                career_uuid UUID REFERENCES careers(career_uuid) NOT NULL,
                studypref_uuid UUID REFERENCES studypreferences(studypref_uuid) NOT NULL,
                studyday_uuid UUID REFERENCES studydays(studyday_uuid) NOT NULL
                                             
                    );
            CREATE TABLE IF NOT EXISTS institutions(
                institution_uuid UUID NOT NULL PRIMARY KEY,
                institution VARCHAR NOT NULL,
                CONSTRAINT institution_unique UNIQUE (institution)
                
                                             
            );   
            CREATE TABLE IF NOT EXISTS qualbookmarks(
                qualbookmark_uuid UUID NOT NULL PRIMARY KEY,
                uuid UUID REFERENCES users(uuid) NOT NULL,
                qual_uuid UUID REFERENCES  qualifications(qual_uuid) NOT NULL
                
                                             
            );                          
            CREATE TABLE IF NOT EXISTS qualifications(
                qual_uuid UUID NOT NULL PRIMARY KEY,
                qual_name VARCHAR(255),
                industry VARCHAR(255) REFERENCES industrys(industry) NOT NULL,
                career VARCHAR(255) REFERENCES careers(career),
                link TEXT NOT NULL, -- "https://croydon.ac.uk/"
                description TEXT NOT NULL,
                qual_icon TEXT NOT NULL,
                institution VARCHAR(255) REFERENCES institutions(institution) NOT NULL, -- Croydon College
                online_freq VARCHAR(255) NOT NULL, -- "2_days_a_week"
                online_freq_label VARCHAR(255) NOT NULL, -- "Online 2 days a week"
                in_person_freq VARCHAR(255) NOT NULL, -- "1_day_a_week"
                in_person_freq_label VARCHAR(255) NOT NULL, -- "In Person 1 day a week"             
                course_length VARCHAR(255) NOT NULL, -- "2_years"
                course_length_label VARCHAR(255) NOT NULL, -- "2 years study"
                earning_potential_lower VARCHAR(255) NOT NULL, --  "60k"
                earning_potential_upper VARCHAR(255) NOT NULL, --  "120k"
                earning_potential_description VARCHAR(255) NOT NULL, -- "no experience needed"
                qual_image VARCHAR(255) NOT NULL,
                CONSTRAINT qual_name_unique UNIQUE (qual_name)
                                             
            );
        
                
            """)

                
                #caesarcrud.caesarsql.run_command("INSERT INTO careers (brand, model, year) VALUES ('Ford', 'Mustang', 1964);")
        except ProgrammingError as pex:
            print(pex)
            if ("the last operation didn't produce a result" in str(pex)):

                pass
            else:
                raise # {"industry":"gaming","career":"game_developer","studypref":"in_person","studydays":"3"}
