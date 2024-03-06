class CaesarCreateTables:
    def __init__(self) -> None:
        self.usersfields = ("uuid","email","password")

        

    def create(self,caesarcrud):
        caesarcrud.create_table("userid",self.usersfields,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL"),
        "usersconnect")


