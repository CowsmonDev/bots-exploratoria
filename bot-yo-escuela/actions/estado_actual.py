import random
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

class EstadoActual:
	datos = OperarArchivo.cargarArchivo("./actions/db/estado_actual.json")
	@staticmethod
	def getCursadas():
		materias = EstadoActual.datos["materias"]["cursadas"]
		retorno = "No estoy cursando nada" if(len(materias) == 0) else "dame un segundo que me acuerde...\nemm, a cierto... estoy cursando:\n"
		for materia in materias:
			retorno += f"- {materia}\n"
		return retorno
	@staticmethod	
	def getFinales():
		finales = EstadoActual.datos["finales"]["en_curso"]
		retorno = "No estoy preparando ningun final" if(len(finales) == 0) else "Estoy preparando:\n\n"
		for final in finales:
			retorno += f"------------- {final['materia']} -------------\n"
			retorno += f"- año: {str(final['año'])}\n"
			retorno += f"- Cuatrimestre: {str(final['cuatrimestre'])}\n"
			retorno += f"- Cursada Aprobada: " + "Si" if (final['cursada_aprobada']) else "No" + "\n"
		return retorno
	@staticmethod
	def getAñoTeorico():
		return EstadoActual.datos["año_teorico"]
	@staticmethod
	def  getAñoActual():
		return EstadoActual.datos["materias"]["año"]
	@staticmethod
	def getAñoIngreso():
		return EstadoActual.datos["año_ingreso"]