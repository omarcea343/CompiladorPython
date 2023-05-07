import sys
import re
import os.path
from enum import Enum
from string import digits

# Lista de palabras reservadas
PALABRAS_RESERVADAS = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean"]

# Definir patrones para los tokens
PATRONES_TOKEN = {
    'operador':r"\-\*|/\*|\*/|\*|/",
    'parentesis': r"[()]",
    'coma': r",",
    'punto_y_coma': r";",
    'comentario_de_linea': r"//.*",
    'comentario_de_bloque': r"/\*.*?\*/",
    'real':  r"\b\d+\.?\d*\b",
    'identificador': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    'llave_abierta': r"\{",
    'llave_cerrada': r"\}",
    'porcentaje': r"\%",
    'simbolos': r'>=|>|<=|<|==|!=|:=|=|--|-|\+\+|\+',
}

# Enumeración para los tipos de token
class TipoToken(Enum):
    PALABRA_RESERVADA = 1
    OPERADOR = 2
    PARENTESIS = 3
    COMA = 4
    PUNTO_Y_COMA = 5
    COMENTARIO_DE_LINEA = 6
    COMENTARIO_DE_BLOQUE = 7
    ENTERO = 8
    REAL = 9
    IDENTIFICADOR = 10
    INCREMENTO = 11
    DECREMENTO = 12
    LLAVE_ABIERTA = 13
    LLAVE_CERRADA = 14
    MAYOR_QUE = 15
    MAYOR_IGUAL = 16
    IGUAL = 17
    IGUAL_IGUAL = 18
    MENOR = 19
    MENOR_IGUAL = 20
    DIFERENTE_DE = 21
    ASIGNACION = 22

def eliminar_comentarios(contenido):
    #Elimina los comentarios de línea y de bloque del contenido.

    contenido = re.sub(PATRONES_TOKEN['comentario_de_linea'], "", contenido)
    contenido = re.sub(PATRONES_TOKEN['comentario_de_bloque'], "", contenido, flags=re.DOTALL)
    return contenido

def procesar_token(descripcion, patron, contenido):
    """
    Procesa los tokens de un tipo específico en el contenido del archivo y devuelve una lista de tuplas con la información de cada token,
    ordenadas por orden de aparición en el archivo.
    """
    tipo_token = next((t for t in TipoToken if t.name.lower() == descripcion.replace(" ", "_").lower()), None)
    for match in re.finditer(patron, contenido):
        token = match.group(0)
        linea = contenido.count('\n', 0, match.start()) + 1
        columna = match.start() - contenido.rfind('\n', 0, match.start())

        yield (match.start(), (token, tipo_token, linea, columna))



def procesar_tokens(contenido):
    """
    Procesa los tokens en el contenido del archivo y devuelve una lista de tuplas con la información de cada token,
    ordenadas por orden de aparición en el archivo.
    """
    tokens_con_posicion = []
    for descripcion, patron in PATRONES_TOKEN.items():
        if descripcion not in ['comentario_de_linea', 'comentario_de_bloque']:                      
            
            if descripcion in ['real']:
                for match in re.finditer(patron, contenido):
                    token = match.group(0)

                    if not token:
                        continue  # Ignorar el token si está vacío

                    try:
                        if "." in token:
                            partes = token.split(".")
                
                            if len(partes) == 2 and partes[1].isdigit():
                                tipo_token = TipoToken.REAL
                            else:
                                raise ValueError("No hay número después del punto decimal")
                        else:
                            tipo_token = TipoToken.ENTERO
                    except ValueError as e:
                        mensaje_error = f"Error léxico: {e} en el token {token}"
                        with open("ErroresLexico.txt", "a") as f:
                            f.write(mensaje_error + "\n")
                        continue  # Ignorar el token si hay un error léxico

                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))

            
            elif descripcion == 'identificador':
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    print("IDENTIF "+token)
                    if token in PALABRAS_RESERVADAS:
                        tipo_token = TipoToken.PALABRA_RESERVADA
                    else:
                        tipo_token = TipoToken.IDENTIFICADOR
                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
            elif descripcion in ['incremento', 'decremento']:
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    tipo_token = TipoToken.INCREMENTO if descripcion == 'incremento' else TipoToken.DECREMENTO
                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
            elif descripcion in ['porcentaje']:
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    tipo_token = TipoToken.OPERADOR
                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
            elif descripcion in ['llave_abierta', 'llave_cerrada']:
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    tipo_token = TipoToken.LLAVE_ABIERTA if descripcion == 'llave_abierta' else TipoToken.LLAVE_CERRADA
                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
            elif descripcion in ['simbolos']:
                 for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    if token == '<':
                        tipo_token = TipoToken.MENOR
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '<=':
                        tipo_token = TipoToken.MENOR_IGUAL
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '>=':
                        tipo_token = TipoToken.MAYOR_IGUAL
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '>':
                        tipo_token = TipoToken.MAYOR_QUE
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '==':
                        tipo_token = TipoToken.IGUAL_IGUAL
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '!=':
                        tipo_token = TipoToken.DIFERENTE_DE
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == ':=':
                        tipo_token = TipoToken.ASIGNACION
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '=':
                        tipo_token = TipoToken.IGUAL
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '--':
                        tipo_token = TipoToken.DECREMENTO
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '-':
                        tipo_token = TipoToken.OPERADOR
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '++':
                        tipo_token = TipoToken.INCREMENTO
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
                    elif token == '+':
                        tipo_token = TipoToken.OPERADOR
                        linea = contenido.count('\n', 0, match.start()) + 1
                        columna = match.start() - contenido.rfind('\n', 0, match.start())
                        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
            else:
                tokens_con_posicion.extend(procesar_token(descripcion, patron, contenido))

    # Ordenar la lista de tuplas por posición en el archivo y devolver solo los tokens
    tokens_ordenados = [token for _, token in sorted(tokens_con_posicion, key=lambda x: x[0])]
    return tokens_ordenados

def leer_archivo(nombre_archivo):
    #Lee el contenido de un archivo.

    if not os.path.isfile(nombre_archivo):
        print("El archivo especificado no existe.")
        sys.exit(1)
    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read()
    return contenido

def imprimir_tokens(tokens):
    """
    Imprime los tokens encontrados.

    Args:
        tokens (list): Una lista de tuplas de tokens.
    """
    print(f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}")
    print("-" * 60)
    for token, tipo_token, linea, columna in tokens:
        tipo = "Palabra reservada" if tipo_token == TipoToken.PALABRA_RESERVADA else tipo_token.name.replace("_", " ").lower()
        print(f"{token:<20} {tipo:<20} {linea:<10} {columna:<10}")

def escribir_tokens_en_archivo(tokens):
    """
    Escribe los tokens encontrados en un archivo de texto.

    Args:
        tokens (list): Una lista de tuplas de tokens.
    """
    with open("ResultadosLexico.txt", "w") as archivo_salida:
        archivo_salida.write(f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}\n")
        archivo_salida.write("-" * 60 + "\n")
        for token, tipo_token, linea, columna in tokens:
            tipo = "Palabra reservada" if tipo_token == TipoToken.PALABRA_RESERVADA else tipo_token.name.replace("_", " ").lower()
            archivo_salida.write(f"{token:<20} {tipo:<20} {linea:<10} {columna:<10}\n")

if __name__ == '__main__':
    # Obtener el nombre del archivo de entrada
    nombre_archivo = sys.argv[1] if len(sys.argv) > 1 else input("Introduce el nombre del archivo: ")
    contenido = leer_archivo(nombre_archivo)
    contenido_sin_comentarios = eliminar_comentarios(contenido)
    
    try:
        # Procesar los tokens en el contenido del archivo sin comentarios
        tokens = procesar_tokens(contenido_sin_comentarios)
        
        # Imprimir y guardar los tokens encontrados
        imprimir_tokens(tokens)
        escribir_tokens_en_archivo(tokens)

    except Exception as e:
        # Escribir el mensaje de error en un archivo de texto
        with open("ErroresLexico.txt", "w") as archivo_errores:
            archivo_errores.write(str(e))
        print("Se ha producido un error durante el procesamiento de los tokens. Consulte el archivo 'ErroresLexico.txt' para más información.")
        