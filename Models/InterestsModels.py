from pydantic import BaseModel

class IndustryInterestsModel(BaseModel):
    industry:str
    career:str
    studypref:str

class IndustryModel(BaseModel):
    industry:str
    label:str
class CareerModel(BaseModel):
    career:str
    label:str
class StudyPrefModel(BaseModel):
    studypref:str
    label:str
class StudyDaysModel(BaseModel):
    studydays:str
    label:str
    # {"industry":"tech","career":"software_developer","studypref":"online","studydays":"3"}