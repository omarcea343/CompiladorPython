import sys
import re
import os.path
from enum import Enum

# Lista de palabras reservadas
PALABRAS_RESERVADAS = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean"]

# Definir patrones para los tokens
PATRONES_TOKEN = {
    'identificador': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    'operador': r"\+\+|--|\+\-|\-\+|\+\*|\-\*|/\*|\*/|:=|[\+\-\*/=<>]",
    'parentesis': r"[()]",
    'coma': r",",
    'punto_y_coma': r";",
    'comentario_de_linea': r"//.*",
    'comentario_de_bloque': r"/\*.*?\*/",
    'entero': r"\b\d+\b",
    'real': r"\b\d+\.\d+\b",
    'llave_abierta': r"\{",
    'llave_cerrada': r"\}",
    'porcentaje': r"\%",
    'asignacion': r":="

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

def eliminar_comentarios(contenido):
    """
    Elimina los comentarios de línea y de bloque del contenido.
    """
    contenido = re.sub(PATRONES_TOKEN['comentario_de_linea'], "", contenido)
    contenido = re.sub(PATRONES_TOKEN['comentario_de_bloque'], "", contenido, flags=re.DOTALL)
    return contenido

def procesar_token(descripcion, patron, contenido):
    """
    Procesa los tokens de un tipo específico en el contenido del archivo y devuelve una lista de tuplas con la información de cada token,
    ordenadas por orden de aparición en el archivo.
    """
    tokens_con_posicion = []
    tipo_token = next((t for t in TipoToken if t.name.lower() == descripcion.replace(" ", "_").lower()), None)
    for match in re.finditer(patron, contenido):
        token = match.group(0)
        linea = contenido.count('\n', 0, match.start()) + 1
        columna = match.start() - contenido.rfind('\n', 0, match.start())
        tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
    return tokens_con_posicion

def procesar_tokens(contenido):
    """
    Procesa los tokens en el contenido del archivo y devuelve una lista de tuplas con la información de cada token,
    ordenadas por orden de aparición en el archivo.
    """
    contenido = eliminar_comentarios(contenido)
    tokens_con_posicion = []
    for descripcion, patron in PATRONES_TOKEN.items():
        if descripcion not in ['comentario_de_linea', 'comentario_de_bloque']:
            if descripcion == 'identificador':
                for match in re.finditer(patron, contenido):
                    token = match.group(0)
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
            elif descripcion in ['asignacion']:
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
            else:
                tokens_con_posicion.extend(procesar_token(descripcion, patron, contenido))

    # Ordenar la lista de tuplas por posición en el archivo y devolver solo los tokens
    tokens_ordenados = [token for _, token in sorted(tokens_con_posicion, key=lambda x: x[0])]
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
    
    try:
        # Procesar los tokens en el contenido del archivo
        tokens = procesar_tokens(contenido)
        
        # Imprimir y guardar los tokens encontrados
        with open("ResultadosLexico.txt", "w") as archivo_salida:
            archivo_salida.write(f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}\n")
            archivo_salida.write("-" * 60 + "\n")
            for token, tipo_token, linea, columna in tokens:
                tipo = "Palabra reservada" if tipo_token == TipoToken.PALABRA_RESERVADA else tipo_token.name.replace("_", " ").lower()
                archivo_salida.write(f"{token:<20} {tipo:<20} {linea:<10} {columna:<10}\n")
                print(f"{token:<20} {tipo:<20} {linea:<10} {columna:<10}")
                if tipo_token == TipoToken.LLAVE_ABIERTA:
                    archivo_salida.write("{:<20} {:<20} {:<10} {:<10}\n".format("{", "Llave abierta", linea, columna))
                    print("{:<20} {:<20} {:<10} {:<10}".format("{", "Llave abierta", linea, columna))
                elif tipo_token == TipoToken.LLAVE_CERRADA:
                    archivo_salida.write("{:<20} {:<20} {:<10} {:<10}\n".format("}", "Llave cerrada", linea, columna))
                    print("{:<20} {:<20} {:<10} {:<10}".format("}", "Llave cerrada", linea, columna)) 
    except Exception as e:
        # Escribir el mensaje de error en un archivo de texto
        with open("ErroresLexico.txt", "w") as archivo_errores:
            archivo_errores.write(str(e))
        print("Se ha producido un error durante el procesamiento de los tokens. Consulte el archivo 'ErroresLexico.txt' para más información.")