class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        result = '  ' * level + self.name + '\n'
        for child in self.children:
            result += child.__str__(level + 1)
        return result


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = 0

    def get_next_token(self):
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            self.token_index += 1

    def eat(self, token_type):
        if self.current_token and self.current_token[1] == token_type:
            self.get_next_token()
        else:
            self.error(token_type)

    def error(self, expected_token_type):
        raise Exception(f"Error de sintaxis. Se esperaba '{expected_token_type}'")

    def programa(self):
        return self.lista_declaracion()

    def lista_declaracion(self):
        node = self.declaracion()
        while self.current_token:
            node2 = self.declaracion()
            node.add_child(node2)
        return node

    def declaracion(self):
        node = Node('declaracion')
        self.eat('IDENTIFICADOR')
        self.eat('PALABRA_RESERVADA')
        return node


# Leer los tokens desde el archivo
tokens = []
with open('resultados.txt', 'r') as file:
    lines = file.readlines()
    for line in lines[2:]:
        token, token_type = line.strip().split('|')
        tokens.append((token.strip(), token_type.strip()))

# Crear el analizador sintáctico y generar el árbol sintáctico
parser = Parser(tokens)
arbol_sintactico = parser.programa()

print('Árbol sintáctico:')
print(arbol_sintactico)
