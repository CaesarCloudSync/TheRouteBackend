class UserInterests:
    def __init__(self) -> None:
        pass
    def getuserinterests(self,useruuid):
        self.userinterestview = f"""
        SELECT users_interests_uuid,users.email,
            industrys.industry,
            industrys.label,
            careers.career,
            careers.label,
            studypreferences.studypref,
            studypreferences.label,
            studydays.studyday,
            studydays.label

            FROM users_interests
            INNER JOIN users ON users_interests.uuid = users.uuid
            INNER JOIN industrys ON users_interests.industry_uuid = industrys.industry_uuid
            INNER JOIN careers ON users_interests.career_uuid = careers.career_uuid
            INNER JOIN studypreferences ON users_interests.studypref_uuid = studypreferences.studypref_uuid
            INNER JOIN studydays ON users_interests.studyday_uuid = studydays.studyday_uuid
            WHERE users.uuid = '{useruuid}';
             
            """
        return self.userinterestview