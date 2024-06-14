from pydantic import BaseModel

class IndustryInterestsModel(BaseModel):
    industry:str
    career:str
    studypref:str
    studydays:str
    # {"industry":"tech","career":"software_developer","studypref":"online","studydays":"3_days_week"}

class IndustryModel(BaseModel):
    industry:str
    label:str
class CareerModel(BaseModel):
    career:str
    label:str
    industry:str
class StudyPrefModel(BaseModel):
    studypref:str
    label:str
class StudyDaysModel(BaseModel):
    studydays:str
    label:str
    # {"industry":"tech","career":"software_developer","studypref":"online","studydays":"3"}