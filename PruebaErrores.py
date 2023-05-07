import sys
import re
import os.path
from enum import Enum
from string import digits

# Definir patrones para los tokens
PATRONES_TOKENS = {
    'IDENTIFICADOR': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    'OPERADOR': r"\-\*|/\*|\*/|\*|/|\+|-",
    'PARENTESIS': r"[()]",
    'COMA': r",",
    'PUNTO_Y_COMA': r";",
    'COMENTARIO_DE_LINEA': r"//.*",
    'COMENTARIO_DE_BLOQUE': r"/\*.*?\*/",
    'REAL':  r"\b\d+(?:\.\d+)?\b",
    'LLAVE_ABIERTA': r"\{",
    'LLAVE_CERRADA': r"\}",
    'MODULO': r"\%",
    'MAYOR_IGUAL': r">=",
    'MAYOR_QUE': r">",
    'MENOR_IGUAL': r"<=",
    'MENOR_QUE': r"<",
    'IGUAL_IGUAL': r"==",
    'DIFERENTE_DE': r"!=",
    'ASIGNACION': r":=",
    'INCREMENTO': r"\+\+",
    'DECREMENTO': r"--",
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

PALABRAS_RESERVADAS = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean"]

def eliminar_comentarios(contenido):
    contenido = re.sub(r"//.*?", "", contenido)
    contenido = re.sub(r"\/\*.*?\*\/", "", contenido, flags=re.DOTALL)
    return contenido

def procesar_token(patron, tipo_token, contenido, errores_lexicos):
    tokens = []
    for match in re.finditer(patron, contenido):
        token = match.group(0)
        linea = contenido.count('\n', 0, match.start()) + 1
        columna = match.start() - contenido.rfind('\n', 0, match.start())

        if tipo_token == "IDENTIFICADOR":
            tipo_token = "PALABRA_RESERVADA" if token in PALABRAS_RESERVADAS else "IDENTIFICADOR"
            if re.match(r"^\d", token):
                errores_lexicos.append(f"Error lexico: el identificador '{token}' no puede comenzar con un numero en la linea {linea}, columna {columna}.")
                continue
            if re.search(r"[^\w]", token):
                errores_lexicos.append(f"Error lexico: el identificador '{token}' contiene caracteres no validos en la linea {linea}, columna {columna}.")
                continue
        elif tipo_token == 'REAL' and not re.match(r"\d+\.\d+\b|\d+\b\.\b\d+|\d+\b", token):
            errores_lexicos.append(f"Error lexico: '{token}' no es un número real valido en la linea {linea}, columna {columna}.")
            continue
        elif tipo_token == 'REAL' and not re.match(r"\d+\.\d+\b", token):
            errores_lexicos.append(f"Error lexico: '{token}' no es un numero real valido en la linea {linea}, columna {columna}.")
            continue

        tokens.append({
            "token": token,
            "tipo": tipo_token,
            "linea": linea,
            "columna": columna,
        })

    return tokens

def procesar_tokens(contenido):
    tokens = []
    errores_lexicos = []

    for tipo_token, patron in PATRONES_TOKENS.items():
        tokens.extend(procesar_token(patron, tipo_token, contenido, errores_lexicos))

    tokens_ordenados = sorted(tokens, key=lambda x: (x["linea"], x["columna"]))
    return tokens_ordenados, errores_lexicos

def leer_archivo(nombre_archivo):
    if not os.path.isfile(nombre_archivo):
        print("El archivo especificado no existe.")
        sys.exit(1)
    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read()
    return contenido

def escribir_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, "w") as archivo_salida:
        archivo_salida.write(contenido)

def imprimir_tokens(tokens):
    print(f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}")
    print("-" * 60)
    for token_tipo in tokens:
        tipo = "Palabra reservada" if token_tipo["tipo"] == "PALABRA_RESERVADA" else token_tipo["tipo"].lower()
        print(f"{token_tipo['token']:<20} {tipo:<20} {token_tipo['linea']:<10} {token_tipo['columna']:<10}")

if __name__ == '__main__':
    nombre_archivo = sys.argv[1] if len(sys.argv) > 1 else input("Introduce el nombre del archivo: ")
    contenido = leer_archivo(nombre_archivo)
    contenido_sin_comentarios = eliminar_comentarios(contenido)
    tokens, errores_lexicos = procesar_tokens(contenido_sin_comentarios)
    imprimir_tokens(tokens)
    escribir_archivo("ResultadosLexico.txt", f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}\n" + "-" * 60 + "\n" + "\n".join([f"{token_tipo['token']:<20} {('Palabra reservada' if token_tipo['tipo'] == 'PALABRA_RESERVADA' else token_tipo['tipo'].lower()):<20} {token_tipo['linea']:<10} {token_tipo['columna']:<10}" for token_tipo in tokens]))
    if errores_lexicos:
        escribir_archivo("ErroresLexico.txt", "\n".join(errores_lexicos))
        print(f"Se han encontrado errores lexicos. Consulte el archivo 'ErroresLexico.txt' para mas informacion.")
    else:
        print("No se han encontrado errores lexicos.")