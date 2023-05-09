import re
import sys

# Lista de palabras reservadas
PALABRAS_RESERVADAS = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "", "cout", "real", "int", "boolean"]

# Definir patrones para los tokens
PATRONES_TOKEN = {
    'operador':r"\-\*|/\*|\*/|\*|/",
    'parentesis': r"[()]",
    'coma': r",",
    'punto_y_coma': r";",
    'real':  r"\b\d+\.\d*\b|\b\d*\.\d+\b",
    'entero': r"\b\d+\b",
    'identificador': r"\b[a-zA-Z_][a-zA-Z0-_]*\b",
    'llave_abierta': r"\{",
    'llave_cerrada': r"\}",
    'porcentaje': r"\%",
    'simbolos': r'>=|>|<=|<|==!=|:=|=|--|-|\+\+|\+',
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
                            tokens.append((valor.upper(), valor, numero_linea))
                        else:
                            tokens.append(('IDENTIFICADOR', valor, numero_linea))
                    elif token_nombre == 'real':
                        tokens.append(('REAL', valor, numero_linea))
                    elif token_nombre == 'entero':
                        tokens.append(('ENTERO', valor, numero_linea))
                    else:
                        tokens.append((token_nombre.upper(), valor, numero_linea))
                    break

            if not match:
                if texto[0] != '\n':
                    errores.append((texto[0], numero_linea))
                texto = texto[1:]

                if texto and texto[0] == '\n':
                    numero_linea += 1

        # Escribir resultados en archivo
        with open(f"{nombre_archivo}_resultados.txt", "w") as archivo_resultados:
            for token in tokens:
                archivo_resultados.write(f"{token[0]:<20} {token[1]:<20} {token[2]:<10}\n")

        # Escribir errores en archivo
        with open(f"{nombre_archivo}_errores.txt", "w") as archivo_errores:
            for error in errores:
                if error[0].strip():
                    archivo_errores.write(f"Error lexico en la linea {error[1]}: {error[0]}\n")

        return tokens

    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no existe")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        nombre_archivo = sys.argv[1]
        tokens = obtener_tokens(nombre_archivo)

        for token in tokens:
            print(token)

    else:
        print("Debe proporcionar el nombre de un archivo como argumento.")
