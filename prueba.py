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

def manejar_error_lexico(mensaje_error):
    print(f"Manejando error léxico: {mensaje_error}")

    # Verificar si el archivo de errores existe
    if not os.path.exists("ErroresLexico.txt"):
        # Si no existe, crear el archivo
        with open("ErroresLexico.txt", "w") as f:
            f.write("Archivo de errores léxicos\n")

    # Escribir el mensaje de error en el archivo
    with open("ErroresLexico.txt", "a") as f:
        f.write(mensaje_error + "\n")

def procesar_tokens(contenido):
    tokens_con_posicion = []
    for descripcion, patron in PATRONES_TOKEN.items():
        if descripcion == 'identificador':
            tipo_token = TipoToken.IDENTIFICADOR
        elif descripcion == 'palabra_reservada':
            tipo_token = TipoToken.PALABRA_RESERVADA
        elif descripcion == 'entero':
            tipo_token = TipoToken.ENTERO
        elif descripcion == 'real':
            tipo_token = TipoToken.REAL
        elif descripcion == 'simbolo':
            tipo_token = TipoToken.SIMBOLO
        else:
            continue
        for match in re.finditer(patron, contenido):
            token = match.group(0)
            if not token:
                continue
            if tipo_token == TipoToken.IDENTIFICADOR:
                if not token.isalnum():
                    with open('ErroresLexico.txt', 'a') as f:
                        f.write(f'Error léxico: el identificador {token} contiene caracteres no alfanuméricos\n')
                    continue
                if token in PALABRAS_RESERVADAS:
                    tipo_token = TipoToken.PALABRA_RESERVADA
            elif tipo_token == TipoToken.REAL:
                if "." in token:
                    partes = token.split(".")
                    if len(partes) == 2 and partes[1].isdigit():
                        tipo_token = TipoToken.REAL
                    else:
                        with open('ErroresLexico.txt', 'a') as f:
                            f.write(f'Error léxico: No hay número después del punto decimal en el token {token}\n')
                        continue
                else:
                    tipo_token = TipoToken.ENTERO
            elif tipo_token == TipoToken.SIMBOLO:
                SIMBOLOS_TOKEN = {
                    '+': TipoToken.SUMA,
                    '-': TipoToken.RESTA,
                    '*': TipoToken.MULTIPLICACION,
                    '/': TipoToken.DIVISION,
                    '=': TipoToken.ASIGNACION,
                    '==': TipoToken.COMPARACION,
                    '!=': TipoToken.DIFERENTE,
                    '<': TipoToken.MENOR_QUE,
                    '>': TipoToken.MAYOR_QUE,
                    '<=': TipoToken.MENOR_IGUAL_QUE,
                    '>=': TipoToken.MAYOR_IGUAL_QUE,
                    '(': TipoToken.PARENTESIS_IZQUIERDO,
                    ')': TipoToken.PARENTESIS_DERECHO,
                    '{': TipoToken.LLAVE_IZQUIERDA,
                    '}': TipoToken.LLAVE_DERECHA,
                    ',': TipoToken.COMA,
                    ';': TipoToken.PUNTO_Y_COMA,
                    '%': TipoToken.MODULO,
                    '++': TipoToken.INCREMENTO,
                    '--': TipoToken.DECREMENTO
                }
                if token in SIMBOLOS_TOKEN:
                    tipo_token = SIMBOLOS_TOKEN[token]
            linea = contenido.count('\n', 0, match.start()) + 1
            columna = match.start() - contenido.rfind('\n', 0, match.start())
            tokens_con_posicion.append((match.start(), (token, tipo_token, linea, columna)))
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
    #Imprime los tokens encontrados.

    print(f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}")
    print("-" * 60)
    for token, tipo_token, linea, columna in tokens:
        tipo = "Palabra reservada" if tipo_token == TipoToken.PALABRA_RESERVADA else tipo_token.name.replace("_", " ").lower()
        print(f"{token:<20} {tipo:<20} {linea:<10} {columna:<10}")

def escribir_tokens_en_archivo(tokens):
    #Escribe los tokens encontrados en un archivo de texto.

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
        