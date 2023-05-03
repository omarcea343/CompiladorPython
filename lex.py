import sys
import re
import os.path

# Lista de palabras reservadas
palabras_reservadas = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean"]

# Definir patrones para los tokens
patron_palabra = r"\b\w+\b"
patron_operador = r"[+\-*/%<>=!]=?|\+\+|--"
patron_parentesis = r"[()\[\]{}]"
patron_coma = r","
patron_punto_coma = r";"
patron_comentario_linea = r"//.*?$"
patron_comentario_bloque = r"/\*[\s\S]*?\*/"

# Obtener el nombre del archivo a leer desde los argumentos de línea de comando
if len(sys.argv) > 1:
    nombre_archivo = sys.argv[1]
else:
    nombre_archivo = input("Introduce el nombre del archivo: ")

# Comprobar si el archivo existe
if not os.path.isfile(nombre_archivo):
    print("El archivo especificado no existe.")
    sys.exit()

# Abrir el archivo y leer su contenido
with open(nombre_archivo, "r") as archivo:
    contenido = archivo.read()

# Encontrar todos los tokens en el contenido del archivo
tokens = list(re.finditer("|".join([patron_palabra, patron_operador, patron_parentesis, patron_coma, patron_punto_coma, patron_comentario_linea, patron_comentario_bloque]), contenido))

archivo = open("nombre_archivo.txt", 'w')
# Imprimir los tokens encontrados
for match in tokens:
    token = match.group(0)
    fila = contenido.count('\n', 0, match.start()) + 1
    columna = match.start() - contenido.rfind('\n', 0, match.start())
    
    if token in palabras_reservadas:
        print(f"'{token}' es una palabra reservada en la fila {fila}, columna {columna}")
        archivo.write(f"'{token}' es una palabra reservada en la fila {fila}, columna {columna}\n")
    elif re.match(patron_palabra, token):
        print(f"'{token}' es un identificador en la fila {fila}, columna {columna}") 
        archivo.write(f"'{token}' es un identificador en la fila {fila}, columna {columna}\n")
    elif re.match(patron_operador, token):
        archivo.write(f"'{token}' es un operador en la fila {fila}, columna {columna}\n")
        print(f"'{token}' es un operador en la fila {fila}, columna {columna}")
    elif re.match(patron_parentesis, token):
        archivo.write(f"'{token}' es un paréntesis en la fila {fila}, columna {columna}\n")
        print(f"'{token}' es un paréntesis en la fila {fila}, columna {columna}")
    elif re.match(patron_coma, token):
        print(f"'{token}' es una coma en la fila {fila}, columna {columna}")
        archivo.write(f"'{token}' es una coma en la fila {fila}, columna {columna}")
    elif re.match(patron_punto_coma, token):
        print(f"'{token}' es un punto y coma")
        archivo.write(f"'{token}' es un punto y coma en la fila {fila}, columna {columna}")
    elif re.match(patron_comentario_linea, token):
        print(f"'{token}' es un comentario de línea")
        archivo.write(f"'{token}' es un comentario de línea en la fila {fila}, columna {columna}")
    elif re.match(patron_comentario_bloque, token):
        print(f"'{token}' es un comentario de bloque")
        archivo.write(f"'{token}' es un comentario de bloque en la fila {fila}, columna {columna}")