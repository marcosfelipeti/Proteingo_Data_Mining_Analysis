import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        conn.close()
 
if __name__ == '__main__':
	create_connection("/scratch/Second_analysis_proteingo/Piccolo_with_features_DB/Piccolo_with_features_DB.db")				