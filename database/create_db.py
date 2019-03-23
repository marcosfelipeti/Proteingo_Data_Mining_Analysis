from __future__ import print_function
import mysql.connector

from mysql.connector import errorcode

#--------------------------------------------------------------------------------------------------------------------------------------------

DB_NAME = 'piccolo_with_features'

#--------------------------------------------------------------------------------------------------------------------------------------------
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

#--------------------------------------------------------------------------------------------------------------------------------------------
def main():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="admin" #Strongly recomend to change root's pasword
	)

	cursor = mydb.cursor()

	try:
		cursor.execute("USE {}".format(DB_NAME))
		print ('Successfully connected to {0} database.'.format(DB_NAME))

	except mysql.connector.Error as err:
		print("Database {} does not exists.".format(DB_NAME))
		if err.errno == errorcode.ER_BAD_DB_ERROR:
			create_database(cursor)
			print("Database {} created successfully.".format(DB_NAME))
			mydb.database = DB_NAME
		else:
			print(err)
			exit(1)

#--------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

	main()	