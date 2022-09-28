from operar_archivo import OperarArchivo

class EstadoActual:
	datos = OperarArchivo.cargarArchivo("./data/estado_carrera/actions/db/estado_actual.json")
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