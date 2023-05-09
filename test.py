import re
import sys

# Diccionario de palabras reservadas
PALABRAS_RESERVADAS = {
    "main": "PALABRA RESERVADA",
    "if": "PALABRA RESERVADA",
    "then": "PALABRA RESERVADA",
    "else": "PALABRA RESERVADA",
    "end": "PALABRA RESERVADA",
    "do": "PALABRA RESERVADA",
    "while": "PALABRA RESERVADA",
    "repeat": "PALABRA RESERVADA",
    "until": "PALABRA RESERVADA",
    "cin": "PALABRA RESERVADA",
    "cout": "PALABRA RESERVADA",
    "real": "PALABRA RESERVADA",
    "int": "PALABRA RESERVADA",
    "boolean": "PALABRA RESERVADA"
}

# Definir patrones para los tokens
PATRONES_TOKEN = {
    'operador':r"\-\*|/\*|\*/|\*|/",
    'parentesis': r"[()]",
    'coma': r",",
    'punto_y_coma': r";",
    'comentario_de_linea': r"//.*",
    'comentario_de_bloque': r"/\*.*?\*/",
    'real':  r"\b\d+\.\d+\b|\b\d+\.\b|\b\.\d+\b",
    'entero': r"\b\d+\b",
    'identificador': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    'llave_abierta': r"\{",
    'llave_cerrada': r"\}",
    'porcentaje': r"\%",
    'simbolos': r'>=|>|<=|<|==|!=|:=|=|--|-|\+\+|\+',
}

def eliminar_comentarios(contenido_archivo):
    # Elim comentarios de línea
    contenido_archivo = re.sub(r"//.*", "", contenido_archivo)

    # Eliminar comentarios de bloque
    contenido_archivo = re.sub(r"/\*.*?\*/", "", contenido_archivo, flags=re.DOTALL)

    return contenido_archivo

def obtener_tokens(nombre_archivo):
    try:
        with open(nombre_archivo) as archivo:
            contenido_archivo = archivo.read()

        contenido_archivo = eliminar_comentarios(contenido_archivo)

        tokens = []
        errores = []

        for numero_linea, linea in enumerate(contenido_archivo.split('\n'), start=1):
            numero_columna = 1

            while linea:
                match = None

                for token_nombre, patron in PATRONES_TOKEN.items():
                    regex = re.compile(patron)
                    match = regex.match(linea)

                    if match:
                        valor = match.group(0)
                        linea = linea[len(valor):]
                        if token_nombre == 'identificador':
                            if valor in PALABRAS_RESERVADAS:
                                tokens.append((valor.lower(), PALABRAS_RESERVADAS[valor], numero_linea, numero_columna))
                            else:
                                if re.match(r"^\d", valor): # Verificar si el identificador comienza con un número
                                    for i, c in enumerate(valor):
                                        if not c.isdigit():
                                            break
                                    tokens.append((valor[:i], 'ENTERO', numero_linea, numero_columna))
                                    tokens.append((valor[i:], 'IDENTIFICADOR', numero_linea, numero_columna + i))
                                else:
                                    tokens.append((valor, token_nombre.upper(), numero_linea, numero_columna))
                        elif token_nombre == 'real':
                            if not re.match(r"^\d+\.\d+$", valor):
                                errores.append((valor, numero_linea, numero_columna))
                            tokens.append((valor, 'REAL', numero_linea, numero_columna))
                        elif token_nombre == 'entero':
                            if not re.match(r"^\d+$", valor):
                                errores.append((valor, numero_linea, numero_columna))
                            tokens.append((valor, 'ENTERO', numero_linea, numero_columna))
                        else:
                            tokens.append((valor, token_nombre.upper(), numero_linea, numero_columna))
                        numero_columna += len(valor)
                        break

                if not match:
                    if linea[0] != '\n':
                        errores.append((linea[0], numero_linea, numero_columna))
                    linea = linea[1:]
                    numero_columna += 1

        # Escribir resultados en archivo
        with open(f"{nombre_archivo}_resultados.txt", "w") as archivo_resultados:
            archivo_resultados.write(f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}\n")
            archivo_resultados.write("-" * 60 + "\n")
            for token in tokens:
                archivo_resultados.write(f"{token[0]:<20} {token[1]:<20} {token[2]:<10} {token[3]:<10}\n")

        # Escribir errores en archivo
        with open(f"{nombre_archivo}_errores.txt", "w") as archivo_errores:
            for error in errores:
                if error[0].strip():
                    archivo_errores.write(f"Error lexico en la linea {error[1]}, columna {error[2]}: {error[0]}\n")

        return tokens

    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no existe")



if __name__ == '____':
    if len(sys.argv) > 1:
        nombre_archivo = sys.argv[1]
        tokens = obtener_tokens(nombre_archivo)

        for token in tokens:
            print(f"{token[0]:<20} {token[1]:<20} {token[2]:<10} {token[3]:<10}")

    else:
        print("Debe proporcionar el nombre de un archivo como argumento.")
