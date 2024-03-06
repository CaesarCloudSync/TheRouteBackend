from caesarsql import CaesarSQL
import pymysql

if __name__ == "__main__":
    caesarsql = CaesarSQL()
    caesarsql.run_command(filename="mysqlsampledatabase.sql")