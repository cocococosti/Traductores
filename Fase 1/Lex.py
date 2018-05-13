"""
Implementación de un analizador lexicográfico para el lenguaje BasicTran

Autores:
Constanza Abarca
Pedro Maldonado

Fecha:
17/05/2018
"""

import ply.lex as lex

# Tokens
tokens = [
	'TkSuma',
	'TkResta',
	'TkId'
]


# Palabras reservadas
reservadas = {
	'with': 'TkWith',
	'end': 'TkEnd'
}

tokens = tokens + list(reservadas.values())

# Ignorar espacios y tabuladores
t_ignore = ' \t'

# Expresiones regulares
t_TkSuma = r'\+' 

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reservadas.get(t.value, 'TkId')
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

def t_error(t):
	print("Error: Caracter inesperado \"" + t.value[0] + "\" en la fila " + str(t.lexer.lineno) + ", columna " + str(get_column(t.lexer.lexdata, t)))
	t.lexer.skip(1)

############ Main ############ 

# Construimos el lexer
lexer = lex.lex()

# Prueba

programa = " with + ?as_a"

lexer.input(programa)

# Extraer tokens

while True:
	tok = lexer.token()

	if not tok:
		break

	print(tok)