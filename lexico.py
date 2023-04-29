import sys
import re
import os.path

# Lista de palabras reservadas
palabras_reservadas = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean"]

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

# Definir una expresión regular para encontrar palabras
patron_palabra = r"\b\w+\b"

# Encontrar todas las palabras en el contenido del archivo
palabras = re.findall(patron_palabra, contenido)

# Imprimir los tokens encontrados
for palabra in palabras:
    if palabra in palabras_reservadas:
        print(f"La palabra '{palabra}' es una palabra reservada.")
    else:
        print(f"La palabra '{palabra}' es un identificador.")
