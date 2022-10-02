import os.path
import json

class OperarArchivo():
	"""@staticmethod
	def guardar(AGuardar):
		with open(".\\actions\\datos","w") as archivo_descarga:
		json.dump(AGuardar, archivo_descarga, indent=4)
		archivo_descarga.close()"""

	@staticmethod
	def cargarArchivo(archivo): 
		retorno = {}
		if os.path.isfile(archivo):
			with open(archivo,"r") as archivo_carga:
				retorno=json.load(archivo_carga)
				archivo_carga.close()
		return retorno