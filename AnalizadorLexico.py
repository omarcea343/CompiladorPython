import sys
import re
import os.path
from enum import Enum

# Lista de palabras reservadas
PALABRAS_RESERVADAS = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean"]

# Definir patrones para los tokens
PATRONES_TOKEN = {
    'identificador': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    'operador': r"[\+\-\*/=<>]",
    'parentesis': r"[()]",
    'coma': r",",
    'punto_y_coma': r";",
    'comentario_de_linea': r"//.*?$",
    'comentario_de_bloque': r"/\*.*?\*/",
    'entero': r"\b\d+\b",
    'real': r"\b\d+\.\d+\b",
    'incremento_decremento': r"\+\+|--"
}

# Enumeración para los tipos de token
class TipoToken(Enum):
    palabra_reservada = 1
    operador = 2
    parentesis = 3
    coma = 4
    punto_y_coma = 5
    comentario_de_linea = 6
    comentario_de_bloque = 7
    entero = 8
    real = 9
    identificador = 10
    incremento_decremento = 11

def procesar_tokens(contenido):
    """
    Procesa los tokens en el contenido del archivo y devuelve una lista de tuplas con la información de cada token,
    ordenadas por orden de aparición en el archivo.
    """
    # Eliminar los comentarios de línea
    contenido = re.sub(PATRONES_TOKEN['comentario_de_linea'], "", contenido)
    # Eliminar los comentarios de bloque
    contenido = re.sub(PATRONES_TOKEN['comentario_de_bloque'], "", contenido, flags=re.DOTALL)

    # Crear una lista de tuplas que contengan el token, su tipo y su posición en el archivo
    tokens_con_posicion = []
    for descripcion, patron in PATRONES_TOKEN.items():
        if descripcion not in ['comentario_de_linea', 'comentario_de_bloque']:
            if descripcion == 'identificador':
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    if token in PALABRAS_RESERVADAS:
                        tipo_token = TipoToken.palabra_reservada
                    else:
                        tipo_token = TipoToken.identificador
                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
            elif descripcion == 'incremento_decremento':
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    tipo_token = TipoToken.incremento_decremento
                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
            else:
                tipo_token = TipoToken[descripcion.replace(" ", "_").lower()]
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
                    linea = contenido.count('\n', 0, match.start()) + 1
                    columna = match.start() - contenido.rfind('\n', 0, match.start())
                    tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))

    # Ordenar la lista de tuplas por posición en el archivo y devolver solo los tokens
    tokens_ordenados = [token for _, token in sorted(tokens_con_posicion)]
    return tokens_ordenados

if __name__ == '__main__':
    # Obtener el nombre del archivo de entrada
    nombre_archivo = sys.argv[1] if len(sys.argv) > 1 else input("Introduce el nombre del archivo: ")
    
    # Verificar si el archivo existe
    if not os.path.isfile(nombre_archivo):
        print("El archivo especificado no existe.")
        sys.exit(1)
    
    # Leer el contenido del archivo
    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read()
    
    # Procesar los tokens en el contenido del archivo
    tokens = procesar_tokens(contenido)
    
    # Imprimir y guardar los tokens encontrados
    with open("ResultadosLexico.txt", "w") as archivo_salida:
        archivo_salida.write("{:<20} {:<20} {:<10} {:<10}\n".format("Token", "Tipo", "Linea", "Columna"))
        archivo_salida.write("-" * 60 + "\n")
        for token, tipo_token, linea, columna in tokens:
            tipo = "Palabra reservada" if tipo_token == TipoToken.palabra_reservada else tipo_token.name.replace("_", " ").lower()
            archivo_salida.write("{:<20} {:<20} {:<10} {:<10}\n".format(token, tipo, linea, columna))
            print("{:<20} {:<20} {:<10} {:<10}".format(token, tipo, linea, columna))
            