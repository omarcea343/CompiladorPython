import re
import sys

# Lista de palabras reservadas
PALABRAS_RESERVADAS = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean"]

# Definir patrones para los tokens
PATRONES_TOKEN = {
    'operador':r"\-\*|/\*|\*/|\*|/",
    'parentesis': r"[()]",
    'coma': r",",
    'punto_y_coma': r";",
    'real':  r"\b\d+\.\d*\b|\b\d*\.\d+\b",
    'entero': r"\b\d+\b",
    'identificador': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    'llave_abierta': r"\{",
    'llave_cerrada': r"\}",
    'porcentaje': r"\%",
    'simbolos': r'>=|>|<=|<|!=|:=|=|--|-|\+\+|\+',
}

def eliminar_comentarios(texto):
    # Elim comentarios de línea
    texto = re.sub(r"//.*", "", texto)

    # Eliminar comentarios de bloque
    texto = re.sub(r"/\*.*?\*/", "", texto, flags=re.DOTALL)

    return texto

def obtener_tokens(nombre_archivo):
    try:
        with open(nombre_archivo) as archivo:
            texto = archivo.read()

        texto = eliminar_comentarios(texto)

        tokens = []
        errores = []
        numero_linea = 1
        numero_columna = 1

        while texto:
            match = None

            for token_nombre, patron in PATRONES_TOKEN.items():
                regex = re.compile(patron)
                match = regex.match(texto)

                if match:
                    valor = match.group(0)
                    texto = texto[len(valor):]
                    if token_nombre == 'identificador':
                        if valor in PALABRAS_RESERVADAS:
                            tokens.append((valor.lower(), "PALABRA RESERVADA", numero_linea, numero_columna))
                        else:
                            tokens.append((valor, token_nombre.upper(), numero_linea, numero_columna))
                    elif token_nombre == 'real':
                        tokens.append((valor, token_nombre.upper(), numero_linea, numero_columna))
                    elif token_nombre == 'entero':
                        tokens.append((valor, token_nombre.upper(), numero_linea, numero_columna))
                    else:
                        tokens.append((valor, token_nombre.upper(), numero_linea, numero_columna))
                    numero_columna += len(valor)
                    break

            if not match:
                if texto[0] != '\n':
                    errores.append((texto[0], numero_linea, numero_columna))
                texto = texto[1:]
                numero_columna += 1

                if texto and texto[0] == '\n':
                    numero_linea += 1
                    numero_columna = 1

        # Escribir resultados en archivo
        with open(f"{nombre_archivo}_resultados.txt", "w") as archivo_resultados:
            archivo_resultados.write(f"{'Token':<20} {'Tipo':<20} {'Linea':<10} {'Columna':<10}\n")
            archivo_resultados.write("-" * 60 + "\n")
            for token in tokens:
                archivo_resultados.write(f"{token[0]:<20} {token[1]:<20} {token[2]:<10} {token[3]:<10}\n")

        # Esbir errores en archivo
        with open(f"{nombre_archivo}_errores.txt", "w") as archivo_errores:
            for error in errores:
                if error[0].strip():
                    archivo_errores.write(f"Error lexico en la linea {error[1]}, columna {error[2]}: {error[0]}\n")

        return tokens

    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no existe")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        nombre_archivo = sys.argv[1]
        tokens = obtener_tokens(nombre_archivo)

        for token in tokens:
            print(f"{token[0]:<20} {token[1]:<20} {token[2]:<10} {token[3]:<10}")

    else:
        print("Debe proporcionar el nombre de un archivo como argumento.")
