from abc import abstractmethod, ABC
import mysql.connector
class Conneccion(ABC) :
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
		

class Client(Conneccion):
	__table : str = "clientes"
	__dni : str = "dni"
	__nombre : str = "nombre"
	__apellido : str = "apellido"
	__cuenta : str = "cuenta"
	__campos : str = __dni + ", " + __nombre + ", " + __apellido + ", " + __cuenta

	def __init__(self) :
		super().__init__()

	def get_campos(self): return self.__campos
	def get_table(self): return self.__table

class Cuenta(Conneccion):
	__table : str = "cuentas"
	__cuenta : str = "cuenta"
	__saldo : str = "saldo"
	__ultimo_movimiento : str = "ultimo_movimiento"
	__campos : str = __cuenta + ", " + __saldo + ", " + __ultimo_movimiento

	def get_datos_cuenta(self, cuenta): 
		res = Conneccion.commit(self, self.get_select() + " WHERE " + self.__cuenta + " = " + cuenta)
		return res


	def get_campos(self): return self.__campos
	def get_table(self): return self.__table