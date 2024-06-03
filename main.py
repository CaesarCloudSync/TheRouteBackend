import uuid
import uvicorn
import hashlib
from dotenv import load_dotenv
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesarhash import CaesarHash
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
from Models.AuthModels import AuthModel
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
async def signup(data: AuthModel):
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
async def login(login_details: AuthModel): # ,authorization: str = Header(None)
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
            user_data = caesarcrud.get_data(("uuid","email"),"users",condition)[0]
            return user_data
        else:
            return {"error":"user does not exist."}
    except Exception as ex:
        return {"error": f"{type(ex)} {str(ex)}"}

#TODO Olisa/Amari - Create, Retrieve, Update and Delete accounts.

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info",host="0.0.0.0")
    #uvicorn.run()
    #asyncio.run(main())