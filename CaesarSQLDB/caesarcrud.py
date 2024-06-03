import base64
from CaesarSQLDB.caesarsql import CaesarSQL
from psycopg import ProgrammingError
class CaesarCRUD:
    def __init__(self) -> None:
        self.caesarsql = CaesarSQL()
 
    def create_table(self,primary_key:str,fields:tuple,types :tuple,table: str):
        if type(fields) == tuple:
            fieldlist = [f"{field} {typestr}"for field,typestr in zip(fields,types)]
            fieldstr = ', '.join(fieldlist)
            try:
                result = self.caesarsql.run_command(f"CREATE TABLE IF NOT EXISTS {table} ({primary_key} serial PRIMARY KEY,{fieldstr});",self.caesarsql.fetch)
            except ProgrammingError as pex:
                if "didn't produce a result" in str(pex):
                    return {"message":f"{table} table was created."}
                else:
                    raise ProgrammingError(pex)


        else:
            fieldstr = f"{fields} {types}"
            try:
                result = self.caesarsql.run_command(f"CREATE TABLE IF NOT EXISTS {table} ({primary_key} serial PRIMARY KEY,{fieldstr});",self.caesarsql.fetch)
            except ProgrammingError as pex:
                if "didn't produce a result" in str(pex):
                    return {"message":f"{table} table was created."}
                else:
                    raise ProgrammingError(pex)
    def base64_to_hex(self,value):
        value = value.encode()
        value = base64.decodebytes(value).hex()
        return value
    

    def post_data(self,fields:tuple,values:tuple,table:str):

            valuestr= str(tuple("%s" for i in values)).replace("'","",100)
            fieldstr = str(tuple(i for i in fields)).replace("'","",100)
            
            if len(fields) == 1:
                fieldstr = fieldstr.replace(",","",100)
                valuestr = valuestr.replace(",","",100)
            #print(f"INSERT INTO {table} {fieldstr} VALUES {valuestr};")

            #values = tuple(map(convert_to_hex,values))

            result = self.caesarsql.run_command(f"INSERT INTO {table} {fieldstr} VALUES {valuestr} returning {fields[0]};",self.caesarsql.fetch,datatuple=values)
            if len(result) != 0:
                return True
            else:
                return False


    def tuple_to_json(self,fields:tuple,result:tuple):
        if type(result[0]) == tuple:
            final_result = []
            for entry in result:
                entrydict = dict(zip(fields,entry))
                final_result.append(entrydict)
            return final_result
        elif type(result[0]) == str:
            final_result = dict(zip(fields,result))
            return final_result 
        
    def json_to_tuple(self,json:dict):
        keys = tuple(json.keys())
        values = tuple(json.values())
        return keys,values


    
    def get_data(self,fields:tuple,table:str,condition=None,getamount:int=1000):
    
        if len(fields) != 1:
            fieldlist = [f"{field}" for field in fields]
            fieldstr = ', '.join(fieldlist) 
        else:
            fieldstr = fields[0]
        
            #fieldstr = fieldstr.replace(", ","",100)
        if condition:
            #print(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            result = self.caesarsql.run_command(f"""SELECT {fieldstr} FROM {table} WHERE {condition} LIMIT {str(getamount)};""",self.caesarsql.fetch)
            if len(result) == 0:
                return False
            elif len(result) != 0 and type(result) == list:
                result = self.tuple_to_json(fields,result)
                return result
            else:
                return {"error":"error syntax error.","error":result}
        else:
            result = self.caesarsql.run_command(f"""SELECT {fieldstr} FROM {table} LIMIT {str(getamount)};""",self.caesarsql.fetch)
            if len(result) == 0:
                return False
            elif len(result) != 0 and type(result) == list:
                result = self.tuple_to_json(fields,result)
                return result
            else:
                return {"error":"error syntax error.","error":result}
    def hex_to_base64(self,hex_file:bytes): # x0 unicode-like hex
        return  base64.b64encode(bytes.fromhex(hex_file.hex())).decode()
    def get_large_data(self,fields:tuple,table:str,condition=None):
    
        if len(fields) != 1:
            fieldlist = [f"{field}" for field in fields]
            fieldstr = ', '.join(fieldlist) 
        else:
            fieldstr = fields[0]
        
            #fieldstr = fieldstr.replace(", ","",100)
        if condition:
            #print(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            result = self.caesarsql.run_command_generator(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            return result
        else:
            result = self.caesarsql.run_command_generator(f"""SELECT {fieldstr} FROM {table};""")
            return result

        
    def update_data(self,fieldstoupdate:tuple,values:tuple,table=str,condition=str):
        if len(fieldstoupdate) > 1:
            updatelist = []
            for field,value in zip(fieldstoupdate,values):
                if type(value) != str:
                    fieldstr = f"{field} = {value}"
                    updatelist.append(fieldstr)

                else:
                    value = value.replace("'","''",1000000)
                    fieldstr = f"{field} = '{value}'"
                    updatelist.append(fieldstr)
            updatestr = ', '.join(updatelist)
            result = self.caesarsql.run_command(f"UPDATE {table} SET {updatestr} WHERE {condition} returning {fieldstoupdate[0]};",self.caesarsql.fetch)
            if len(result) == 0:
                return True
            else:
                return False
        else:          
            if type(values[0]) != str:
                updatestr = f"{fieldstoupdate[0]} = {values[0]}"
            else:
                value = values[0].replace("'","''",1000000)
                updatestr = f"{fieldstoupdate[0]} = '{value}'"
            result = self.caesarsql.run_command(f"UPDATE {table} SET {updatestr} WHERE {condition} returning {fieldstoupdate[0]};",self.caesarsql.fetch)
            if len(result) == 0:
                return True
            else:
                return False
    # TODO Cgeck This works
    def update_blob(self,fieldstoupdate:str,value:str,table=str,condition=str):
        updatestr = "UPDATE %s SET %s = x'%s' WHERE %s returning %s;" % (table,fieldstoupdate,self.base64_to_hex(value),condition,fieldstoupdate[0])
        result = self.caesarsql.run_command(updatestr,self.caesarsql.fetch)
        if len(result) == 0:
            return True
        else:
            return False
    def delete_data(self,table:str,condition:str):
        field_name = condition.split("=")[0].strip()
        result = self.caesarsql.run_command(f"DELETE FROM {table} WHERE {condition} returning {field_name};",self.caesarsql.fetch)
        if len(result) == 0:
            return True
        else:
            return False
        
    def check_exists(self,fields:tuple,table:str,condition=None):
        if len(fields) != 1:
            fieldlist = [f"{field}" for field in fields]
            fieldstr = ', '.join(fieldlist) 
        else:
            fieldstr = fields[0]
        
            #fieldstr = fieldstr.replace(", ","",100)
        if condition:
            #print(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            result = self.caesarsql.run_command(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""",self.caesarsql.check_exists)
            if result == True or result == False:
                return result
            else:
                return {"message":"syntax error or table doesn't exist.","error":result}
                
        else:
            result = self.caesarsql.run_command(f"""SELECT {fieldstr} FROM {table};""",self.caesarsql.check_exists)
            if result == True or result == False:
                return result
            else:
                return {"message":"syntax error or table doesn't exist.","error":result}

    
