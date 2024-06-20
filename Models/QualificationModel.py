from pydantic import BaseModel

class InstitutionModel(BaseModel):
    institution:str
class QualificationModel(BaseModel):
    qual_name:str
    industry:str
    career:str
    link:str
    description:str
    qual_icon:str
    institution:str
    online_freq:str
    online_freq_label:str
    in_person_freq:str
    in_person_freq_label:str            
    course_length:str
    course_length_label:str
    earning_potential_lower:str
    earning_potential_upper:str
    earning_potential_description:str
    qual_image:str