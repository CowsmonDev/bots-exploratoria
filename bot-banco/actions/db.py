import mysql.connector
class Conneccion :
	__db_host : str = "localhost"
	__db_user : str = "agustin"
	__db_password : str = "Agustin@22-23"
	__db_database : str = "bot_banco"
	def __init__(self) :
		self.__conn = mysql.connector.connect(host = Conneccion.__db_host, username=Conneccion.__db_user, password=Conneccion.__db_password, database=Conneccion.__db_database)
	def commit(self,sql):
		cursor = self.__conn.cursor(buffered=True)
		try:
			cursor.execute(sql)
			self.__conn.commit()
			res = cursor.fetchall()
		except mysql.connector.Error as e:
			print ("Error code:", e.errno)        # error number
			print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
			print ("Error message:", e.msg)       # error message
			print ("Error:", e)                   # errno, sqlstate, msg values
			s = str(e)
			print ("Error:", s)
		return res

class Client(Conneccion):
	__table : str = "clientes"
	__dni : str = "dni"
	__nombre : str = "nombre"
	__apellido : str = "apellido"
	__cuenta : str = "cuenta"
	__campos : str = __dni + ", " + __nombre + ", " + __apellido + ", " + __cuenta

	def __init__(self) :
		super().__init__()

	def select(self):
		res = Conneccion.commit(self, "SELECT " + Client.__campos + " FROM " + Client.__table)
		return res


"""
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
"""