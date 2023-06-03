# Definición de constantes
TYPE = 'PALABRA_RESERVADA'
ID = 'IDENTIFICADOR'
COMMA = 'COMA'
SEMICOLON = 'PUNTO_Y_COMA'

# Clase para representar un token
class Token:
    def __init__(self, token_type, value, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

# Función para leer los tokens desde el archivo
def read_tokens(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        # Omitir las primeras dos líneas del archivo (encabezado)
        next(file)
        next(file)

        for line in file:
            token_values = line.strip().split('|')
            if len(token_values) == 3:
                value, token_type, position = map(str.strip, token_values)
                line_number, column_number = map(str.strip, position.split(','))
                line_number = int(line_number.split()[1])
                column_number = int(column_number.split()[1])
                tokens.append(Token(token_type, value, line_number, column_number))
            else:
                print(f'Error en el formato del archivo de tokens: {line}')
                break
    return tokens

# Función para realizar el análisis sintáctico
def parse(tokens):
    index = 0
    while index < len(tokens):
        token = tokens[index]
        
        if token.token_type == TYPE:
            if index + 1 < len(tokens) and tokens[index + 1].token_type == ID:
                variable_name = tokens[index + 1].value
                index += 2
                if index < len(tokens) and tokens[index].token_type == SEMICOLON:
                    print(f'Declaración de variable: {variable_name} en línea {tokens[index].line}, columna {tokens[index].column}')
                    index += 1
                else:
                    print(f'Error de sintaxis: se esperaba un {SEMICOLON} en línea {tokens[index].line}, columna {tokens[index].column}')
            else:
                print(f'Error de sintaxis: se esperaba un identificador en línea {tokens[index].line}, columna {tokens[index].column}')
                index += 1
        else:
            print(f'Error de sintaxis: se esperaba un tipo de dato en línea {tokens[index].line}, columna {tokens[index].column}')
            index += 1

# Ruta del archivo de tokens
file_path = 'resultados.txt'

# Obtener tokens desde el archivo
tokens = read_tokens(file_path)

# Realizar el análisis sintáctico
parse(tokens)
