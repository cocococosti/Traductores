"""
Implementación de un analizador lexicográfico para el lenguaje BasicTran

Autores:
Constanza Abarca
Pedro Maldonado

Fecha:
17/05/2018
"""

import ply.lex as lex
from sys import argv

# Tokens
tokens = [
	'TkComa',
	'TkPunto',
	'TkDosPuntos',
	'TkParAbre',
	'TkParCierra',
	'TkCorcheteAbre',
	'TkCorcheteCierra',
	'TkLlaveAbre',
	'TkLlaveCierra',
	'TkHacer',
	'TkAsignacion',
	'TkSuma',
	'TkResta',
	'TkMult',
	'TkDiv',
	'TkConjuncion',
	'TkDisyuncion',
	'TkMenor',
	'TkMenorIgual',
	'TkMayor',
	'TkMayorIgual',
	'TkIgual',
	'TkSiguienteCar',
	'TkAnteriorCar',
	'TkValorAscii',
	'TkConcatenacion',
	'TkShift',
	'TkId',
	'TkNum',
	'TkError',
	'TkErrorSol'
]


# Palabras reservadas
reservadas = {
	'with': 'TkWith',
	'begin': 'TkBegin',
	'var': 'TkVar',
	'int': 'TkInt',
	'bool': 'TkBool',
	'char': 'TkChar',
	'array': 'TkArray',
	'of': 'TkOf',
	'true': 'TkTrue',
	'false': 'TkFalse',
	'if': 'TkIf',
	'otherwise': 'TkOtherwise',
	'while': 'TkWhile',
	'for': 'TkFor',
	'from': 'TkFrom',
	'to': 'TkTo',
	'step': 'TkStep',
	'read': 'TkRead',
	'print': 'TkPrint',
	'not': 'TkNot',
	'end': 'TkEnd'
}

tokens = tokens + list(reservadas.values())

# Ignorar espacios y tabuladores
t_ignore = ' \t'

# Expresiones regulares

t_TkComa = r'\,'
t_TkPunto = r'\.'
t_TkDosPuntos = r'\:'
t_TkParAbre = r'\('
t_TkParCierra = r'\)'
t_TkCorcheteAbre = r'\['
t_TkCorcheteCierra = r'\]'
t_TkLlaveAbre = r'\{'
t_TkLlaveCierra = r'\}'
t_TkHacer = r'\->'
t_TkAsignacion = r'\<-'
t_TkSuma = r'\+'
t_TkResta = r'\-'
t_TkMult = r'\*'
t_TkDiv = r'\/'
t_TkConjuncion = r'\/\\' 
t_TkDisyuncion = r'\\/'
t_TkMenor = r'\<'
t_TkMenorIgual = r'\<='
t_TkMayor = r'\>'
t_TkMayorIgual = r'\>='
t_TkIgual = r'\='
#DESIGUAL
t_TkSiguienteCar = r'[+][+]'
t_TkAnteriorCar = r'[-][-]'
t_TkValorAscii = r'\#'
t_TkConcatenacion = r'[:][:]'
t_TkShift = r'\$'
t_TkErrorSol = r'.'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_TkError(t):
	r'[^a-zA-Z_0-9<+()[]][0-9]*[a-zA-Z_][a-zA-Z_0-9]*'
	t.value = t.value[0]
	t.lexer.error = True
	t.type = 'TkError'
	return t


	

def t_error(t):
	#print("Error: Caracter inesperado \"" + t.value[0] + "\" en la fila " + str(t.lexer.lineno) + ", columna " + str(get_column(t.lexer.lexdata, t)))
	#t.lexer.error = True
	t.lexer.skip(1)

def t_TkChar(t):
	r'[\']([\n]{1}|[\t]{1}|[\']{1}|[\\t]{1}|[\\]{1}|.{1})[\']'
	t.type = 'TkChar'
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reservadas.get(t.value, 'TkId')
	return t

def t_TkNum(t):
	r'\d+'
	t.value = int(t.value)
	return t


def get_column(entrada, token):
	# El atributo lexpos es un entero que contiene la posicion actual en el texto de
	# entrada (justo despues del ultimo texto matcheado)
	# Con rfind hallamos el index del ultimo salto de linea antes de la posicion actual
	# y le sumamos 1 para obtener el index del inicio de la linea actual
	inicio = entrada.rfind('\n', 0, token.lexpos) + 1
	# Al index de la posicion actual con respecto a todo el texto le restamos el index
	# del inicio de la linea actual (con respecto a todo el texto) y asi obtenemos la
	# posicion actual con respecto a la linea
	column = (token.lexpos - inicio) + 1
	return column




############ Main ############ 

# Construimos el lexer
lexer = lex.lex()
lexer.error = False

# Prueba

programa = '''
with + as_a 2\/
+
hola
if
if
'''

otro = '''
with
	var (ifHola : int
	+
	++++
	7hola
	'ad'

begin
	contador <- 35 .


end
'''

filename = argv[1]

program = ""

with open(filename, 'r') as fd:
	for line in fd:
		program = program + line


lexer.input(otro)
contador = 0
error = False
for tok in lexer:
	if tok.type == 'TkError' or tok.type == 'TkErrorSol':
		error = True
	pass

lexer.lexpos = 0
lexer.lineno = 0
lines = {} 
n = 0
if (error):
	for tok in lexer:
		if tok.type == 'TkError' or tok.type == 'TkErrorSol':
			print("Error: Caracter inesperado \"" + tok.value + "\" en la fila " + str(lexer.lineno) + ", columna " + str(get_column(lexer.lexdata, tok)))
else:
	for tok in lexer:

		if (str(tok.lineno) in lines):
			if (tok.type == 'TkId'):
				lines[str(tok.lineno)].append(tok.type + "(\"" + tok.value + "\") " + str(tok.lineno) + " " + str(get_column(lexer.lexdata, tok)))
			else:
				lines[str(tok.lineno)].append(tok.type + " " + str(tok.lineno) + " " + str(get_column(lexer.lexdata, tok)))
		else:
			if (tok.type == 'TkId'):
				lines[str(tok.lineno)] = [tok.type + "(\"" + tok.value + "\") " + str(tok.lineno) + " " + str(get_column(lexer.lexdata, tok))]
			else:
				lines[str(tok.lineno)] = [tok.type + " " + str(tok.lineno) + " " + str(get_column(lexer.lexdata, tok))]
	
	for val in range(1,lexer.lineno):
		i = 0
		if str(val) in lines:
			for j in lines[str(val)]:
				if (i == len(lines[str(val)])-1):
					print(j)
				else:
					print(j + ", ", end = '')
				i = i + 1

'''
FALTA
- que pasa si encuentra un numero negativo: lo lee como numero, o como TkResta y TkNum?
- matchear error cuando aparece un solo caracter invalido, por ejemplo una linea con un solo ?
- palabras resrvadas sensibles a mayusculas?
- preguntar sobre inconsistencia en el conteo de las lineas del ejemplo.
- preguntar cuantas columnas ocupa el tab? si es un solo caracter no deberia ocupar una sola col?
'''
