from caesarsql import CaesarSQL
import pandas as pd
import os
import shutil

def insert_data():
# Insert Data into Table resume
    for ind,candidate in enumerate(names):
        data_exists = caesarsql.run_command(f"SELECT name FROM {table} WHERE name LIKE '{candidate}'",caesarsql.check_exists)
        if not data_exists:
            amarilogo = caesarsql.convert_to_blob(f"Logos/{logos[ind]}")
            amaricv = caesarsql.convert_to_blob(f"Humans/{humans[ind]}")
            resumetuple = (candidate,amarilogo,amaricv)
            caesarsql.run_command(f"INSERT INTO {table} (name,photo,resume) VALUES (%s,%s,%s)",datatuple=resumetuple)
            print("resume inserted.")
if __name__ == "__main__":
   #allnames = pd.read_csv("brazilian-names.csv")
   names = ['Issa', 'Midas', 'Adalvina', 'Euquenor', 'Celimena', 'Poguira', 'Munir', 'Corina', 'Vismara', 'Tristão', 'Baraúna', 'Pandora', 'Náiade', 'Salatiel', 'Jênie', 'Pasini', 'Acalântis', 'Platâo', 'Xanthe', 'Bretãs', 'Branka', 'Marina', 'Moke', 'Natacha', 'Saladino', 'Silvana', 'Libânia', 'Fedro', 'Tito', 'Bosco', 'Barac', 'Abdera', 'Daltivo', 'Elvira', 'Iodâmia', 'Jacina', 'Carmem', 'Osni', 'Metanira', 'Afrodísio', 'Lindoia', 'Abner', 'Samir', 'Ramão', 'Agabo', 'Norina', 'Inandê', 'Zebilon', 'Solveig', 'Telêmaco', 'Fauno', 'Aranha', 'Holda', 'Alan', 'Marisa', 'Apolínio', 'Alexandre', 'Keike', 'Haskel', 'Cinara', 'Sátiro', 'Vincent', 'Epicasta', 'Odélio', 'Karolina', 'Alex', 'Wolf', 'Arthur', 'Dona', 'Faros', 'Santoro', 'Nery', 'Fernandes', 'Partênope', 'Faetonte', 'Caron', 'Angerona', 'Fenaio', 'Mandi', 'Amapola', 'Kauê', 'Seth', 'Dimitre', 'Astêmio', 'Ira', 'Kanela', 'Onã', 'Almirante', 'Carol', 'Cezar', 'Adina', 'Beoto', 'Ida', 'Tecobiara', 'Urbano', 'Aritana', 'Solange', 'Górki', 'Apolline', 'Oberon']
   logos = os.listdir("Logos")
   humans = os.listdir("Humans")[:100]
   db = "resumebase"
   table = "resumes"
   caesarsql = CaesarSQL()
   # Create Database
   db_exists = caesarsql.run_command(f"SHOW DATABASES LIKE '{db}';",caesarsql.check_exists)
   if not db_exists:
    caesarsql.run_command(f"CREATE DATABASE {db};")
   caesarsql.run_command(f"USE {db};")
# Create Table resume
   table_exists = caesarsql.run_command(f"SHOW TABLES LIKE '{table}';",caesarsql.check_exists)
   if not table_exists:
    caesarsql.run_command(f"CREATE TABLE {table} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), photo BLOB,resume MEDIUMBLOB)")

      

   candidate = "Amari Lawal Again"
   newcandidate = "Amari Lawal"
   data_exists = caesarsql.run_command(f"SELECT name FROM {table} WHERE name LIKE '{newcandidate}'",caesarsql.check_exists)
   if data_exists:
      result = caesarsql.run_command(f"SELECT name from {table} WHERE name LIKE '{newcandidate}'",caesarsql.fetch)
      print(result)
      #caesarsql.run_command(f"UPDATE {table} SET name='{newcandidate}' WHERE name LIKE '{candidate}'")
      #print("table update.")
