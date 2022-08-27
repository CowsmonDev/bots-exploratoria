import mysql.connector
def dataInsert(FirstName, LastName):
	mydb = mysql.connector.connect(
		host='localhost',
		user='agustin',
		password='Agustin@22-23',
		database='prueba'
	)

	mycursor = mydb.cursor()
	sql = 'INSERT INTO tabla (nombre, apellido) VALUES ("{0}", "{1}");'.format(FirstName, LastName)
	mycursor.execute(sql)
	mydb.commit()