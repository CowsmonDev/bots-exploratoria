
from data.modules.operar_archivo import OperarArchivo

def getFinalText(final):
	retorno = ""
	retorno += f"------------- {final['materia']} -------------\n"
	retorno += f"- año: {str(final['año'])}\n"
	retorno += f"- Cuatrimestre: {str(final['cuatrimestre'])}\n"
	retorno += f"- Cursada Aprobada: " + "Si" if (final['cursada_aprobada']) else "No" + "\n"
	retorno += f"----------------------------------------------\n"
	return retorno


class EstadoActual:
	datos = OperarArchivo.cargarArchivo("./data/estado_carrera/actions/db/estado_actual.json")
	@staticmethod
	def getCursadas(): # ya esta
		materias = EstadoActual.datos["materias"]["cursadas"]

		if(len(materias) == 0):
			return "No estoy cursando nada"
		
		retorno =  "dame un segundo que me acuerde...\nemm, a cierto... estoy cursando:\n"
		for materia in materias:
			retorno += f"- {materia}\n"
		return retorno

	@staticmethod	
	def getFinalesEnCurso(): # ya esta
		finales = EstadoActual.datos["finales"]["en_curso"]

		if(len(finales) == 0):
			return "No estoy preparando ningun final"

		retorno = "Estoy preparando:\n\n"
		for final in finales:
			retorno += getFinalText(final)
		return retorno

	@staticmethod
	def getFinalesPendientes():
		finales_curso = EstadoActual.datos["finales"]["en_curso"]
		finales_pendientes = EstadoActual.datos["finales"]["pendientes"]

		if(len((finales_curso)) == 0 and (len(finales_pendientes) == 0)):
			return "No tengo ningun final pendiente"

		retorno = "Estoy Preparando:\n\n"
		for final in finales_curso: 
			retorno += getFinalText(final)
		for final in finales_pendientes:
			retorno += getFinalText(final)
		return retorno

	@staticmethod
	def getAñoTeorico():
		return EstadoActual.datos["año_teorico"] # ya esta
	@staticmethod
	def  getAñoActual():
		return EstadoActual.datos["materias"]["año"] # ya esta