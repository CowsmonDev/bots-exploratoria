materia(6111, 1, 1, 'Introduccion a la Programacion 1').
materia(6112, 1, 1, 'Analisis Matematico 1').
materia(6113, 1, 1, 'Algebra').
materia(6114, 1, 1, 'Quimica').
materia(6121, 1, 2, 'Ciencias de la Computacion 1').
materia(6122, 1, 2, 'Introduccion a la Programacion 2').
materia(6123, 1, 2, 'Algebra Lineal'). 
materia(6124, 1, 2, 'Fisica General'). 
materia(6125, 1, 2, 'Matematica Discreta'). 
materia(6211, 2, 1, 'Ciencias de la Computacion 2'). 
materia(6212, 2, 1, 'Analisis y Diseño de Algoritmos 1'). 
materia(6213, 2, 1, 'Introduccion a la arquitecuta de Sistemas'). 
materia(6214, 2, 1, 'Analisis Matematico 2'). 
materia(6215, 2, 1, 'Electricidad y Magnetismo'). 
materia(6221, 2, 2, 'Analisis y Diseño de Algoritmos 2'). 
materia(6222, 2, 2, 'Comunicacion de Datos 1'). 
materia(6223, 2, 2, 'Probabilidad y Estadistica'). 
materia(6224, 2, 2, 'Electronica Digital'). 
materia(6225, 2, 2, 'Ingles'). 
materia(6311, 3, 1, 'Programacion Orientada a Objetos'). 
materia(6312, 3, 1, 'Estructura de Almacenamiento de Datos'). 
materia(6313, 3, 1, 'Metodologias del Desarrollo de Software 1'). 
materia(6314, 3, 1, 'Arquitectura de Computadoras 1'). 
materia(6321, 3, 2, 'Programacion Exploratoria'). 
materia(6322, 3, 2, 'Base de datos 1'). 
materia(6323, 3, 2, 'Lenguajes de Programacion 1'). 
materia(6324, 3, 2, 'Sistemas Operativos 1'). 
materia(6325, 3, 2, 'Investigacion Operativa 1'). 
materia(6411, 4, 1, 'Arquitectura de Computadores y Tecnicas Digitales'). 
materia(6412, 4, 1, 'Teoria de la Informacion'). 
materia(6413, 4, 1, 'Comunicacion de Datos 2'). 
materia(6414, 4, 1, 'Introducccion al Calculo Diferencial e Integral'). 
materia(6415, 4, 1, 'Ciclo de Especializacion'). 
materia(6421, 4, 2, 'Diseño de Sistemas de Software'). 
materia(6422, 4, 2, 'Diseño de Compiladores 1'). 
materia(6423, 4, 2, 'Ciclo de Especializacion'). 
materia(6511, 5, 1, 'Ingeñeria de Software'). 
materia(6512, 5, 1, 'Ciclo de Especializacion'). 
materia(6521, 5, 2, 'Practicas Profesionales Supervisadas'). 
materia(6522, 5, 2, 'Proyecto Final'). 

correlativas(6111, []).
correlativas(6112, []).
correlativas(6113, []).
correlativas(6114, []).
correlativas(6121, []).
correlativas(6122, [6111]).
correlativas(6123, [6113]).
correlativas(6124, [6112]).
correlativas(6125, [6113]).
correlativas(6211, [6121, 6122, 6125]).
correlativas(6212, [6121, 6122, 6125]).
correlativas(6213, [6122]).
correlativas(6214, [6112]).
correlativas(6215, [6124]).
correlativas(6221, [6211, 6212]).
correlativas(6222, [6213]).
correlativas(6223, [6214, 6123, 6125]).
correlativas(6224, [6215]).
correlativas(6225, [6221]).
correlativas(6311, [6221]).
correlativas(6312, [6221, 6223]). 
correlativas(6313, [6221]). 
correlativas(6314, [6213, 6224]). 
correlativas(6321, [6221]). 
correlativas(6322, [6312, 6313]). 
correlativas(6323, [6311]). 
correlativas(6324, [6312, 6314]). 
correlativas(6325, [6214, 6223]). 
correlativas(6411, [6314]). 
correlativas(6412, [6212, 6222, 6223]). 
correlativas(6413, [6222, 6324]). 
correlativas(6414, [6214]). 
correlativas(6415, []). 
correlativas(6421, [6311, 6322, 6324]). 
correlativas(6422, [6323]). 
correlativas(6423, []). 
correlativas(6511, [6421]). 
correlativas(6512, []). 
correlativas(6521, []). 
correlativas(6522, []). 

materia_aprobada(6111).
materia_aprobada(6112).
materia_aprobada(6113).
materia_aprobada(6114).
materia_aprobada(6121).
materia_aprobada(6122).
materia_aprobada(6123).
materia_aprobada(6124).
materia_aprobada(6125).
materia_aprobada(6211).
materia_aprobada(6212).
materia_aprobada(6213).
materia_aprobada(6214).
materia_aprobada(6215).
materia_aprobada(6221).
materia_aprobada(6223).
materia_aprobada(6225).

materia_aprobada(X,Y,W,Z) :- materia_aprobada(X), materia(X,Y,W,Z).

materia_final_aprobada(6111).
materia_final_aprobada(6112).
materia_final_aprobada(6113).
materia_final_aprobada(6114).
materia_final_aprobada(6121).
materia_final_aprobada(6122).
materia_final_aprobada(6123).
materia_final_aprobada(6124).
materia_final_aprobada(6125).
.
materia_final_aprobada(6211).
materia_final_aprobada(6212).
materia_final_aprobada(6213).
materia_final_aprobada(6215).
materia_final_aprobada(6225).

materia_final_aprobada(X,Y,W,Z) :- materia_aprobada(X,Y,W,Z), materia_final_aprobada(X).