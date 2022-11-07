from abc import abstractmethod, ABC
import mysql.connector

class Conneccion:
	__db_host : str = "localhost"
	__db_user : str = "agustin"
	__db_password : str = "Agustin@22-23"
	__db_database : str = "bot_personas"
	def __init__(self) :
		self.__conn = mysql.connector.connect(host = Conneccion.__db_host, username=Conneccion.__db_user, password=Conneccion.__db_password, database=Conneccion.__db_database)
	def commit(self,sql):
		cursor = self.__conn.cursor(buffered=True)
		try:
			cursor.execute(sql)
			self.__conn.commit()
			res = cursor.fetchall()
			return res
		except mysql.connector.Error as e:
			print ("Error code:", e.errno)        # error number
			print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
			print ("Error message:", e.msg)       # error message
			print ("Error:", e)                   # errno, sqlstate, msg values
			s = str(e)
			print ("Error:", s)
		return None 
	def get_select(self): return "SELECT " + self.get_campos() + " FROM " + self.get_table()
	def select(self):
		res = self.commit(self, self.get_select(self))
		return res
	
	@abstractmethod
	def get_campos(self): pass
	@abstractmethod
	def get_table(self): pass

class PersonasDB(Conneccion):

	__table : str = "personas"
	__id_conversacion: str = "id_conversacion"
	__numero : str = "numero"
	__nombre : str = "nombre"
	__profesion : str = "profesion"
	__campos : str = f"{__id_conversacion}, {__numero}, {__nombre}, {__profesion}"

	def existe_persona(self, id_conversacion): 
		res = Conneccion.commit(self, self.get_select() + " WHERE " + self.__id_conversacion + " = " + str(id_conversacion))
		return res

	def agregar_persona(self, datos):
		Conneccion.commit(self, f"INSERT INTO {self.__table} ({self.get_campos()}) VALUES ({datos[0]}, {datos[1]}, {datos[2]}, {datos[3]})")

	def get_campos(self): return self.__campos
	def get_table(self): return self.__table