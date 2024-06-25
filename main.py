import uuid
import uvicorn
import hashlib
from dotenv import load_dotenv
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union,Optional
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesarhash import CaesarHash
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
from Models.AuthModels import SignupAuthModel,LoginAuthModel
from Models.InterestsModels import IndustryInterestsModel,IndustryModel,CareerModel,StudyDaysModel,StudyPrefModel
from Models.QualificationModel import QualificationModel,InstitutionModel
from SQLQueries.sqlqueries import UserInterests
from iteration_utilities import unique_everseen
from Models.Bookmarks import StoreQualificationBookMarkModel
load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesarcrud = CaesarCRUD()
btdjwt = CaesarJWT(caesarcrud)
caesarcreatetables = CaesarCreateTables()
caesarcreatetables.create(caesarcrud)
JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "BTD Connect API."
@app.post('/api/v1/signupapi') # POST
async def signup(data: SignupAuthModel):
    try:
        data = data.model_dump()
        hashed = hashlib.sha256(data["password"].encode('utf-8')).hexdigest()
        data["password"] = hashed
        table = "users"
        condition = f"email = '{data['email']}'"
        email_exists = caesarcrud.check_exists(("*"),table,condition=condition)
        if email_exists:
            return {"message": "Email already exists"} # , 400
        elif not email_exists:
            user_uuid = str(uuid.uuid4())
            res = caesarcrud.caesarsql.run_command(f"INSERT INTO users (uuid,email,password,first_name,last_name,date_of_birth) VALUES ('{user_uuid}', '{data['email']}', '{data['password']}','{data['first_name']}','{data['last_name']}','{data['date_of_birth']}');")
            if res:
                access_token = btdjwt.secure_encode({"uuid":user_uuid})#create_access_token(identity=signupdata["email"])
                callback = {"status": "success","access_token":access_token}
            else:
                return {"error":"error when posting signup data."}
            return callback
    except Exception as ex:
        error_detected = {"error": "error occured","errortype":type(ex), "error": str(ex)}
        print(error_detected)
        return error_detected
@app.post('/api/v1/loginapi') # POST
async def login(login_details: LoginAuthModel): # ,authorization: str = Header(None)
    # Login API
    try:

        login_details = dict(login_details)
        #print(login_details)
        condition = f"email = '{login_details['email']}'"
        email_exists = caesarcrud.check_exists(("*"),"users",condition=condition)
        if email_exists:
         
            access_token = btdjwt.provide_access_token(login_details)
            if access_token == "Wrong password":
                return {"message": "The username or password is incorrect."}
            else:
                return {"access_token": access_token}
        else:
            return {"message": "The username or password is incorrect."}
    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}

@app.get('/api/v1/getuserinfo') # POST
async def getuserinfo(authorization: str = Header(None)): # ,authorization: str = Header(None)
    try:
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        condition = f"uuid = '{current_user}'"
        user_exists = caesarcrud.check_exists(("*"),"users",condition=condition)
        if user_exists:
            user_data = caesarcrud.get_data(("email","first_name","last_name","date_of_birth"),"users",condition)[0]
            return user_data
        else:
            return {"error":"user does not exist."}
    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}
@app.delete('/api/v1/deleteuser') # POST
async def deleteuser(authorization: str = Header(None)): # ,authorization: str = Header(None)
    try:
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        condition = f"uuid = '{current_user}'"
        user_exists = caesarcrud.check_exists(("*"),"users",condition=condition)
        if user_exists:
            print("hello")
            # TODO Delete
            caesarcrud.delete_data("users",condition)
            return {"message":"user was deleted."}
        else:
            return {"error":"user does not exist."}
    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}
# Store interests
@app.post('/api/v1/storeuserinterests') # POST
async def storeinterests(industry_interests: IndustryInterestsModel,authorization: str = Header(None)): # ,authorization: str = Header(None)
    # Login API
    try:
        industry_interests = industry_interests.model_dump()
        industry = industry_interests["industry"]
        career = industry_interests["career"]
        studypref = industry_interests["studypref"]
        studydays = industry_interests["studydays"]
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        condition = f"uuid = '{current_user}'"
        user_exists = caesarcrud.check_exists(("*"),"users",condition=condition)
        print(current_user)
        if user_exists:
            user_interests_exists = caesarcrud.check_exists(("*"),"users_interests",condition=f"uuid = '{current_user}'")
            if user_interests_exists:
                return {"error":"user interest already exists"}
            else:
                users_interests_uuid = str(uuid.uuid4())
                career_uuid,industry_uuid,studypref_uuid,studyday_uuid= caesarcrud.caesarsql.run_command(f"SELECT careers.career_uuid,industrys.industry_uuid,studypreferences.studypref_uuid,studydays.studyday_uuid FROM careers,industrys,studypreferences,studydays WHERE careers.career = '{career}' AND industrys.industry = '{industry}' AND studypreferences.studypref = '{studypref}' AND studydays.studyday = '{studydays}';",result_function=caesarcrud.caesarsql.fetch)[0]
                caesarcrud.caesarsql.run_command(f"INSERT INTO users_interests (users_interests_uuid,uuid,career_uuid,industry_uuid,studypref_uuid,studyday_uuid) VALUES ('{users_interests_uuid}','{current_user}','{career_uuid}','{industry_uuid}','{studypref_uuid}','{studyday_uuid}');")
                return {'message':'user interests stored.'}

    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}
@app.get("/api/v1/getindustrychoices")
async def getindustrychoices():
    try:
        careers = []
        industrys = []
        studyprefs = []
        studydays = []
        # Better error checking is needed here for data that doesn't exist

        industry_choices_lists = caesarcrud.caesarsql.run_command(f"SELECT careers.career,careers.label,industrys.industry,industrys.label,studypreferences.studypref,studypreferences.label,studydays.studyday,studydays.label FROM careers,industrys,studypreferences,studydays WHERE careers.industry = industrys.industry;",result_function=caesarcrud.caesarsql.fetch)
        for choice  in industry_choices_lists:
            career_value = choice[0]
            career_label = choice[1]

            industry_value = choice[2]
            industry_label = choice[3]
                        
            studypref_value = choice[4]
            studypref_label = choice[5]
                        
            studydays_value = choice[6]
            studydays_label = choice[7]
            
            careers.append({"value":career_value,"label":career_label,"industry":industry_value})
            industrys.append({"value":industry_value,"label":industry_label})
            studyprefs.append({"value":studypref_value,"label":studypref_label})
            studydays.append({"value":studydays_value,"label":studydays_label})
        career_choices = {}

        # Iterate over each item in the input data
        industries = []
        for item in careers:
            # Get the industry of the current item
            industry = item['industry']
            
            # Create the industry key in the output dictionary if it doesn't already exist
            if industry not in career_choices:
                career_choices[industry] = []
            
            # Create a new dictionary with 'label' and 'value' keys
            new_item = {
                'label': item['label'],
                'value': item['value']
            }
            industries.append(industry)
            # Append the new dictionary to the list corresponding to the industry key
            career_choices[industry].append(new_item)
        final_career = {}
        for industry in industries:
            final_career[industry] = list(unique_everseen(career_choices[industry]))

            
            

        #print(final_career)
    
        return {"careers":final_career,"industrys":list(unique_everseen(industrys)),"studyprefs":list(unique_everseen(studyprefs)),"studydays":list(unique_everseen(studydays))} 
    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}
# Storing Interest entities
@app.post('/api/v1/storeindustryentity') # POST
async def storeindustryentity(industry_model: IndustryModel): # ,authorization: str = Header(None)
    # Login API
    try:
        industry_model = industry_model.model_dump()
        industry = industry_model['industry']
        label = industry_model["label"]
        condition = f"industry = '{industry}'"
        industry_exists = caesarcrud.check_exists(("*"),"industrys",condition=condition)
        if industry_exists:
            return {"message":"industry already exists."}
        else:
            industry_uuid = str(uuid.uuid4())
            res = caesarcrud.caesarsql.run_command(f"INSERT INTO industrys (industry_uuid,industry,label) VALUES ('{industry_uuid}','{industry}','{label}');")
            return {"message":"industry was inserted."}
    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}
@app.post('/api/v1/storecareerentity') # POST
async def storecareerentity(career_model: CareerModel): # ,authorization: str = Header(None)
    # Login API
    try:
        career_model = career_model.model_dump()
        career = career_model['career']
        label = career_model["label"]
        industry = career_model["industry"]
        condition = f"career = '{career}'"
        career_exists = caesarcrud.check_exists(("*"),"careers",condition=condition)
        if career_exists:
            return {"message":"career already exists."}
        else:
            career_uuid = str(uuid.uuid4())

            res = caesarcrud.caesarsql.run_command(f"INSERT INTO careers (career_uuid,career,label,industry) VALUES ('{career_uuid}','{career}','{label}','{industry}');")
            return {"message":"career was inserted."}
    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}
@app.post('/api/v1/storestudyprefentity') # POST
async def storestudyprefentity(studyprefs_model: StudyPrefModel): # ,authorization: str = Header(None)
    # Login API
    try:
        studyprefs_model = studyprefs_model.model_dump()
        studyprefs = studyprefs_model['studypref']
        label = studyprefs_model["label"]
        condition = f"studypref = '{studyprefs}'"
        studyprefs_exists = caesarcrud.check_exists(("*"),"studypreferences",condition=condition)
        if studyprefs_exists:
            return {"message":"studypref already exists."}
        else:
            studyprefs_uuid = str(uuid.uuid4())
            res = caesarcrud.caesarsql.run_command(f"INSERT INTO studypreferences (studypref_uuid,studypref,label) VALUES ('{studyprefs_uuid}','{studyprefs}','{label}');")
            return {"message":"studypref was inserted."}
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.post('/api/v1/storestudydayentity') # POST
async def storestudydayentity(studydays_model: StudyDaysModel): # ,authorization: str = Header(None)
    # Login API
    try:
        studydays_model = studydays_model.model_dump()
        studydays = studydays_model['studydays']
        label = studydays_model["label"]
        condition = f"studyday = '{studydays}'"
        studydays_exists = caesarcrud.check_exists(("*"),"studydays",condition=condition)
        if studydays_exists:
            return {"message":"studyday already exists."}
        else:
            studydays_uuid = str(uuid.uuid4())
            res = caesarcrud.caesarsql.run_command(f"INSERT INTO studydays (studyday_uuid,studyday,label) VALUES ('{studydays_uuid}','{studydays}','{label}');")
            return {"message":"studyday was inserted."}
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.post('/api/v1/storeinstitution') # POST
async def storeinstitution(institution_model: InstitutionModel): # ,authorization: str = Header(None)
    # Login API
    try:
        institution_model = institution_model.model_dump()
        institution = institution_model['institution']
        condition = f"institution = '{institution}'"
        institution_exists = caesarcrud.check_exists(("*"),"institutions",condition=condition)
        if institution_exists:
            return {"message":"institution already exists."}
        else:
            institution_uuid = str(uuid.uuid4())
            res = caesarcrud.caesarsql.run_command(f"INSERT INTO institutions (institution_uuid,institution) VALUES ('{institution_uuid}','{institution}');")
            return {"message":"institution was inserted."}
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}

@app.post('/api/v1/storequalification') # POST
async def storequalification(qualification_model: QualificationModel): # ,authorization: str = Header(None)
    # Login API
    try:
        qualification_model = qualification_model.model_dump()
        qual_name = qualification_model['qual_name']
        industry = qualification_model['industry']
        career = qualification_model['career']
        link = qualification_model['link']
        description = qualification_model['description']
        qual_icon = qualification_model['qual_icon']
        institution = qualification_model['institution']
        online_freq = qualification_model["online_freq"]
        online_freq_label = qualification_model["online_freq_label"]
        in_person_freq = qualification_model["in_person_freq"]
        in_person_freq_label = qualification_model["in_person_freq_label"]          
        course_length = qualification_model["course_length"]
        course_length_label = qualification_model["course_length_label"]
        earning_potential_lower = qualification_model["earning_potential_lower"]
        earning_potential_upper = qualification_model["earning_potential_upper"]
        earning_potential_description = qualification_model["earning_potential_description"]
        qual_image = qualification_model["qual_image"]
        condition = f"qual_name = '{qual_name}' AND institution = '{institution}'"
        qualification_exists = caesarcrud.check_exists(("*"),"qualifications",condition=condition)
        if qualification_exists:
            return {"message":"qualification already exists."}
        else:
            qual_uuid = str(uuid.uuid4())
            industry_exists = caesarcrud.check_exists(("*"),"industrys",condition=f"industry = '{industry}'")
            if not industry_exists:
                return {"error":"industry does not exist."}

            career_exists = caesarcrud.check_exists(("*"),"careers",condition=f"career = '{career}'")
            if career_exists:
              
                res = caesarcrud.caesarsql.run_command(f"""INSERT INTO qualifications (qual_uuid,qual_name,industry,career,
                    link,
                    description,
                    qual_icon,
                    institution,
                    online_freq,
                    online_freq_label,
                    in_person_freq,
                    in_person_freq_label,            
                    course_length,
                    course_length_label,
                    earning_potential_lower,
                    earning_potential_upper,
                    earning_potential_description,
                    qual_image) VALUES ('{qual_uuid}','{qual_name}','{industry}','{career}',
                    '{link}',
                    '{description}',
                    '{qual_icon}',
                    '{institution}',
                    '{online_freq}',
                    '{online_freq_label}',
                    '{in_person_freq}',
                    '{in_person_freq_label}',            
                    '{course_length}',
                    '{course_length_label}',
                    '{earning_potential_lower}',
                    '{earning_potential_upper}',
                    '{earning_potential_description}',
                    '{qual_image}');""")
                return {"message":"qualifcation was inserted."}
            else:
                return {"error":"career does not exist."}
                # insert new career here then insert data
            
            #res = caesarcrud.caesarsql.run_command(f"INSERT INTO studydays (studyday_uuid,studyday,label) VALUES ('{studydays_uuid}','{studydays}','{label}');")
       
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}

@app.get('/api/v1/getqualifications') # POST
async def getqualifications(offset:int): # ,authorization: str = Header(None)
    # Login API
    try:
        offset = offset- 1
        res = caesarcrud.caesarsql.run_command(f"SELECT * FROM qualifications LIMIT 8 OFFSET {offset};",result_function=caesarcrud.caesarsql.fetch)
        #print("hello",res)
        if len(res) != 0:
            qualifications = caesarcrud.tuple_to_json(caesarcreatetables.qualifications_columns,res)
            return {"qualifications":qualifications}
        else:
            if offset <= 8:
                return {"error":"no qualifications exist in the database."}
            else:
                return {"offsetend":"true"}
            
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.get('/api/v1/getcareerfilter') # POST
async def getcareerfilter(offset:int,industry:Optional[str] = None): # ,authorization: str = Header(None)
    # Login API
    try:
        offset = offset- 1
        if not industry:
            res = caesarcrud.caesarsql.run_command(f"SELECT career,label,industry FROM careers LIMIT 8 OFFSET {offset};",result_function=caesarcrud.caesarsql.fetch)
        else:
            res = caesarcrud.caesarsql.run_command(f"SELECT career,label,industry FROM careers WHERE industry = '{industry}' LIMIT 8 OFFSET {offset} ;",result_function=caesarcrud.caesarsql.fetch)
        if len(res) != 0:
            careers = caesarcrud.tuple_to_json(("career","label","industry"),res)
            print(careers)
            return {"filters":careers}
        else:
            if offset <= 8:
                return {"error":"no qualifications exist in the database."}
            else:
                return {"offsetend":"true"}
            
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.get('/api/v1/searchqualifications') # POST
async def searchqualifications(text:str): # ,authorization: str = Header(None)
    # Login API
    try:
        #offset = offset - 1
        #print(text)
        res = caesarcrud.caesarsql.run_command(f"SELECT * FROM qualifications WHERE qual_name ILIKE '%{text}%' OR institution ILIKE '%{text}%' LIMIT 30;",result_function=caesarcrud.caesarsql.fetch) # OFFSET {offset}
        #print("hello",res)
        if len(res) != 0:
            qualifications = caesarcrud.tuple_to_json(caesarcreatetables.qualifications_columns,res)
            return {"qualifications":qualifications}
        else:
          
            return {"error":"no qualifications exist in the database."}
    
            
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.get('/api/v1/getuserinterestqualifications') # POST
async def getuserinterestqualifications(offset:int,authorization: str = Header(None)): # ,authorization: str = Header(None)
    # Login API
    try:
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        offset = offset- 1
        res = caesarcrud.caesarsql.run_command(f"""
        SELECT 
        qualifications.qual_uuid ,
        qualifications.qual_name,
        qualifications.industry,
        qualifications.career,
        qualifications.link ,
        qualifications.description,
        qualifications.qual_icon,
        qualifications.institution,
        qualifications.online_freq,
        qualifications.online_freq_label,
        qualifications.in_person_freq,
        qualifications.in_person_freq_label,          
        qualifications.course_length, 
        qualifications.course_length_label,
        qualifications.earning_potential_lower,
        qualifications.earning_potential_upper,
        qualifications.earning_potential_description,
        qualifications.qual_image

        FROM careers
        INNER JOIN users_interests ON users_interests.career_uuid = careers.career_uuid
        INNER JOIN qualifications ON qualifications.career= careers.career
    
        WHERE users_interests.uuid = '{current_user}';                               
        """,result_function=caesarcrud.caesarsql.fetch) # LIMIT 8 OFFSET {offset};
        #print("hello",res)
        if len(res) != 0:
            qualifications = caesarcrud.tuple_to_json(caesarcreatetables.qualifications_columns,res)
            return {"qualifications":qualifications}
        else:
            if offset <= 8:
                return {"error":"no qualifications exist in the database."}
            else:
                return {"offsetend":"true"}
            
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.get('/api/v1/getuserinterests') # POST
async def getuserinterests(authorization: str = Header(None)): # ,authorization: str = Header(None)
    # Login API
    try:
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        userintsql = UserInterests()
        res = caesarcrud.caesarsql.run_command(userintsql.getuserinterests(current_user),result_function=caesarcrud.caesarsql.fetch)
        if len(res) != res:
            user_interests = caesarcrud.tuple_to_json(("users_interests_uuid","email",
            "industry",
            "industry_label",
            "career",
            "careers_label",
            "studypref",
            "studypref_label",
            "studyday",
            "studydays_label"),res)[0]
            return user_interests
        else:
            return {"error":"user interest does not exist."}
        print(res)
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.post('/api/v1/storequalificationbookmark') # POST
async def storequalificationbookmark(qual_uuid_model:StoreQualificationBookMarkModel,authorization: str = Header(None)): # ,authorization: str = Header(None)
    # Login API
    try:
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        qual_uuid_model = qual_uuid_model.model_dump()
        qual_uuid = qual_uuid_model["qual_uuid"]
        qual_bookmark_exists =caesarcrud.check_exists(("*"),"qualbookmarks",condition=f"uuid = '{current_user}' AND qual_uuid = '{qual_uuid}'")
        if qual_bookmark_exists:
            return {"message":"qualification bookmark already exists"}
        else:
            qualbookmark_uuid = str(uuid.uuid4())
            caesarcrud.post_data(("qualbookmark_uuid","uuid","qual_uuid"),(qualbookmark_uuid,current_user,qual_uuid),"qualbookmarks")
            return {"message":"qualification was inserted."}
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.delete('/api/v1/removequalificationbookmark') # POST
async def removequalificationbookmark(qual_uuid:str,authorization: str = Header(None)): # ,authorization: str = Header(None)
    # Login API
    try:
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        qual_bookmark_exists =caesarcrud.check_exists(("*"),"qualbookmarks",condition=f"uuid = '{current_user}' AND qual_uuid = '{qual_uuid}'")
        if qual_bookmark_exists:
            caesarcrud.delete_data("qualbookmarks",f"uuid = '{current_user}' AND qual_uuid = '{qual_uuid}'")
            return {"message":"qualification bookmark was removed"}
        else:

            return {"error":"qualification does not exist in bookmark."}
    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
@app.get('/api/v1/getbookmarkedqualifications') # POST
async def getbookmarkedqualifications(authorization: str = Header(None)): # ,authorization: str = Header(None)
    # Login API
    try:
        current_user = btdjwt.secure_decode(authorization.replace("Bearer ",""))["uuid"]
        qualbookmarks_exists = caesarcrud.check_exists(("*"),"qualbookmarks",condition=f"uuid = '{current_user}'")
        if qualbookmarks_exists:
            res = caesarcrud.caesarsql.run_command(f"""
            SELECT 
            qualifications.qual_uuid ,
            qualifications.qual_name,
            qualifications.industry,
            qualifications.career,
            qualifications.link ,
            qualifications.description,
            qualifications.qual_icon,
            qualifications.institution,
            qualifications.online_freq,
            qualifications.online_freq_label,
            qualifications.in_person_freq,
            qualifications.in_person_freq_label,          
            qualifications.course_length, 
            qualifications.course_length_label,
            qualifications.earning_potential_lower,
            qualifications.earning_potential_upper,
            qualifications.earning_potential_description,
            qualifications.qual_image

            FROM qualifications
            INNER JOIN qualbookmarks ON qualbookmarks.qual_uuid = qualifications.qual_uuid
      
            WHERE qualbookmarks.uuid = '{current_user}';
    """,result_function=caesarcrud.caesarsql.fetch)
            
            quals_bookmarked = caesarcrud.tuple_to_json(caesarcreatetables.qualifications_columns,res)
            return {"qual_bookmarks":quals_bookmarked}
        else:
            return {"nobookmarks":"no book marks"}

    except Exception as ex:
         print(ex)
         return {"error": f"{type(ex)} {str(ex)}"}
if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info",host="0.0.0.0")
    #uvicorn.run()
    #asyncio.run(main())