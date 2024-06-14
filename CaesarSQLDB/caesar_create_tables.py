from CaesarSQLDB.caesarcrud import CaesarCRUD
from psycopg import ProgrammingError
import uuid
class CaesarCreateTables:
    def __init__(self) -> None:
        pass
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
                industry VARCHAR(255) REFERENCES industrys(industry) NOT NULL
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
                
            """)

                
                #caesarcrud.caesarsql.run_command("INSERT INTO careers (brand, model, year) VALUES ('Ford', 'Mustang', 1964);")
        except ProgrammingError as pex:
            print(pex)
            if ("the last operation didn't produce a result" in str(pex)):

                pass
            else:
                raise # {"industry":"gaming","career":"game_developer","studypref":"in_person","studydays":"3"}
