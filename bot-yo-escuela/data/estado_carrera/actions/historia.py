from swiplserver import PrologMQI, PrologThread

def getFinalText(final):
	retorno = f"~/ {final['NM']}\n"
	return retorno

class Historia:

	@staticmethod
	def getConsulta(consulta):
			with PrologMQI(port=8000) as mqi:
				with mqi.create_thread() as prolog_thread:
					prolog_thread.query_async("consult('~/GitHub/bots-exploratoria/bot-yo-escuela/data/estado_carrera/actions/db/historia.pl')", find_all=False)
					prolog_thread.query_async(consulta, find_all=True)
					result = prolog_thread.query_async_result()
					return result

	@staticmethod
	def getMaterias():
		impresion = "--------------------------------------------\n"
		impresion += "| Te paso la lista porque no me acuerdo :) |\n"
		impresion += "--------------------------------------------\n\n"
		res = Historia.getConsulta("materia(M,X,Y,Z)")
		for x in res:
			impresion += f"{x['M']} - {x['X']} - {x['Y']} - {x['Z']}"
		return impresion


	@staticmethod
	def getFinalesAprobados():
		impresion = "--------------------------------------------\n"
		impresion += "| Te paso la lista porque no me acuerdo :) |\n"
		impresion += "|------------------------------------------|\n"
		impresion += "|            ~/--APROBE--\\~                |\n"
		impresion += "--------------------------------------------\n\n"
		res = Historia.getConsulta(f"materia_final_aprobada(CM,Y,CU,NM)")
		for final in res:
			impresion += getFinalText(final)
		impresion += "   Si, tengo una lista preparada con mis finales (para que se vea bonito) :)   "
		return impresion

	@staticmethod
	def getMateriasAprobadas():
		impresion = "--------------------------------------------\n"
		impresion += "| Te paso la lista porque no me acuerdo :) |\n"
		impresion += "|------------------------------------------|\n"
		impresion += "|            ~/--APROBE--\\~                |\n"
		impresion += "--------------------------------------------\n\n"
		res = Historia.getConsulta(f"materia_aprobada(CM,Y,CU,NM")
		for cursada in res:
			impresion += getFinalText(cursada)
		impresion += "   Si, tengo una lista preparada con mis finales (para que se vea bonito) :)   "
		return impresion
