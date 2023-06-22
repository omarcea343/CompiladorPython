from nltk.tree import Tree
from globall import TokenType
from globall import TreeNode
import sys
import os
from parseH import *
token = -1
source = open('Archivo_Tokens2.txt','r')
tokenString = ''
root = Tree('program',[])
lineno = 0
colpos = 0
fileSintax = open(os.path.join(os.getcwd(),'Errores_Sintaxis.txt'),'w')
import inspect

def sintaxError(msg:str):
    global lineno
    #caller = inspect.currentframe().f_back.f_code.co_name
    fileSintax.write("Sintax error at line: {} message:{}\n".format(lineno,msg))


def match(expected:TokenType):
    global token
    global tokenString
    if( token == expected):
        token = getTokenSintax()
    else:
        caller = inspect.currentframe().f_back.f_code.co_name
        sintaxError("Unexpected token -> " + tokenString + "   match "+caller)
    
def list_dec()->Tree:
    global token
    t = Tree('lista de dec',[])
    p = t.extend(dec())
    caller = inspect.currentframe().f_back.f_code.co_name
    print(f"list_dec {caller}")
    while( token != TokenType.ENDFILE.value  and token != TokenType.END.value
          and token != TokenType.UNTIL.value and token != TokenType.ELSE.value
          and token != TokenType.RBPAREN.value):
        print(f"lst {caller}")
        
        
        q = dec()
        t.extend(q)   
    if(len(t) == 0):
        t = Tree('',[])
    #sintaxError('aaaa '+caller)
    return t

def dec()->Tree:
    global token
    t = Tree('',[])
    print("dec")
    
    if ( token == TokenType.INT.value or token == TokenType.REAL.value or token == TokenType.BOOLEAN.value):
       
        t = dec_var()
    else:
       
        t = lista_stmt()
    return t

def dec_var()->Tree:
    global token 
    t = Tree('Declaracion',[])
    e = Tree('Declaracion',[])
    global tokenString
    print("dec_var")
    
    if( token == TokenType.INT.value ):
       
        e.append(Tree(str(TokenType.INT.name),[]))
        match(TokenType.INT.value)
    elif ( token == TokenType.BOOLEAN.value ):
        e.append(Tree(str(TokenType.BOOLEAN.name),[]))
        match(TokenType.BOOLEAN.value)
    elif( token == TokenType.REAL.value ):
       
        e.append(Tree(str(TokenType.REAL.name),[]))
        match(TokenType.REAL.value)
    else:
        sintaxError('Date Type Unknown')
        token = getTokenSintax()
    
    e.append(lista_ids())
    #if( token == TokenType.ID.value ):
    #    t.append(Tree(tokenString,[]))   
    #match(TokenType.ID.value)
    #while ( token == TokenType.COMMA.value ):
    #    match(TokenType.COMMA.value)
    #    if( token == TokenType.ID.value ):
    #        t.append(Tree(tokenString,[]))
    #        match(TokenType.ID.value)   
        
    if( token == TokenType.SEMMICOL.value ):
        
        match(TokenType.SEMMICOL.value)
    else:
        sintaxError('unexpectd token')
    t.append(e)    
    return t

def lista_ids()->Tree:
    global token
    global tokenString
    print("list_ids")
    
    t = Tree('',[])
    if( token == TokenType.ID.value ):
        t = Tree('Variable',[])
        t.append(Tree(tokenString,[]))
        match(TokenType.ID.value)
        while( token == TokenType.COMMA.value ):
           
            match(TokenType.COMMA.value)
            if( token == TokenType.ID.value ):
                t.append(Tree(tokenString,[]))
                match(TokenType.ID.value)

    return t

import inspect
def lista_stmt()->Tree: #Aqui debería de haber un opcionalidad de un nodo vacio
    global token 
    global tokenString
    caller = inspect.currentframe().f_back.f_code.co_name
    print("lista_stmt "+ str(TokenType(token).name)+' '+caller)
    
    t = Tree('Lista de stmt',[])
    if(token == TokenType.MAIN.value or token == TokenType.IF.value or token==TokenType.DO.value or token == TokenType.WHILE.value or token == TokenType.CIN.value or token == TokenType.COUT.value or token == TokenType.ID.value or token == TokenType.LESSL.value or token == TokenType.PLUSP.value):
        t = Tree('Lista de stmt',[])
        while( token == TokenType.MAIN.value or token == TokenType.IF.value or token==TokenType.DO.value or token == TokenType.WHILE.value or token == TokenType.CIN.value or token == TokenType.COUT.value or token == TokenType.ID.value or token == TokenType.LESSL.value or token == TokenType.PLUSP.value):
            t.append(statement())
    
    else:
        t = Tree('',[])
        print("Unexpected Token "+ str(token))
        sintaxError("Unexpected Token "+' '+ tokenString)
        token = getTokenSintax()

        
    return t


def statement()->Tree:
    global token 
    t = Tree('',[])
    print("stmt")
    
    if ( token == TokenType.MAIN.value ):
        t = main_stmt()
    elif( token == TokenType.IF.value ):
        t = if_stmt()
    elif( token == TokenType.DO.value):
        t = rep_stmt()
    elif( token == TokenType.WHILE.value ):
        t = it_stmt()
    elif( token == TokenType.CIN.value ):
        t = cin_stmt()
    elif( token == TokenType.COUT.value):
        t = cout_stmt()
    elif( token == TokenType.ID.value or token == TokenType.LESSL.value or token == TokenType.PLUSP.value ): 
        t = assign_stmt()
    else:
        sintaxError('Unexpected Token ->')
        token = getTokenSintax() 
    return t
def main_stmt()->Tree:
    print("main")
    
    t  = Tree('Main',[])
    match(TokenType.MAIN.value)
    match(TokenType.LBPAREN.value)
    t.extend(list_dec())
    match(TokenType.RBPAREN.value)
   
    return t
def assign_stmt()->Tree:
    global token
    global tokenString
    t = Tree('Assign',[])
    if( token == TokenType.PLUSP.value or token == TokenType.LESSL.value):
        t.extend(assign_pre())
    elif( token == TokenType.ID.value ):
        t.extend(assign_simple())
    #match(TokenType.SEMMICOL.value)
    return t
    
def assign_simple()->Tree:
    global token
    global tokenString
    print("assign")
    
    t = Tree('Assign',[])
    if( token == TokenType.ID.value):
        t.append(Tree(tokenString,[]))
    match(TokenType.ID.value)
    if( token == TokenType.ASSIGN.value ):
        match(TokenType.ASSIGN.value)
        t.extend(stmt_exp()) #Por que t[0] ?? y falta un if --------------------------------------------------------------
        
    elif( token == TokenType.LESSL.value or token == TokenType.PLUSP.value ):
        t.extend(assign_post())
    else:
        t.append(Tree('',[]))
        
    return t
def assign_pre()->Tree:
    global token
    global tokenString
    t = Tree('Assign',[])
    t.append(Tree(tokenString,[]))
    match(token)
    if ( token == TokenType.ID.value ):
        t[0].append(Tree(tokenString,[]))
        match(TokenType.ID.value)
        match(TokenType.SEMMICOL.value)
           
    else:
        sintaxError("Unexpected Token "+ tokenString)
        token = getTokenSintax()
    return t
def assign_post()->Tree:
    global token
    global tokenString
    t = Tree('Assign',[])
    t.append(Tree(tokenString,[]))
    match(token)
    if( token == TokenType.PLUSP.value or token == TokenType.LESSL.value):
        t[0].append(Tree(tokenString,[]))
        match(token)
        match(TokenType.SEMMICOL.value)
           
    else:
        sintaxError("Unexpected Token "+ tokenString)
        token = getTokenSintax()
    return t
def stmt_exp()->Tree:
    global token 
    t = Tree('sent_expresion',[])
  
    print("stmt_exp")
    
    if( token == TokenType.SEMMICOL.value ):
        t.append(Tree(';',[]))
        match(TokenType.SEMMICOL.value)
    else:
        t.append(exp())
        match(TokenType.SEMMICOL.value)
    return t

def if_stmt()->Tree:
    global token 
    print("if")
    
    t = Tree('If',[])
    match(TokenType.IF.value)
    t.append(exp())
    t.extend(list_dec())
    if ( token == TokenType.ELSE.value ):
        match(TokenType.ELSE.value)
        e = Tree('Else',[])
        e.extend(list_dec())
        t.append(e)
    match(TokenType.END.value)
    return t

def it_stmt()->Tree:
    global token
    print("while")
     
    t = Tree('Iteracion while',[])
    match(TokenType.WHILE.value)
    t.append(exp())
    match(TokenType.LBPAREN.value)
    t.extend(list_dec())
    match(TokenType.RBPAREN.value)
    return t

def rep_stmt()->Tree:
    global token
    global tokenString
    print("do")
     
    t = Tree('Repeticion do',[])
    match(TokenType.DO.value)
    t.append(list_dec())
    match(TokenType.UNTIL.value)
    t.append(exp())
    
    match(TokenType.SEMMICOL.value)
    return t


def cin_stmt()->Tree:
    global token
    t = Tree('Cin',[])
    global tokenString
    match(TokenType.CIN.value)
    if( token == TokenType.ID.value ):
        t.append(Tree(tokenString,[]))
    match(TokenType.ID.value)
    match(TokenType.SEMMICOL.value)
    return t

def cout_stmt()->Tree:
    global token 
    t = Tree('Cout',[])
    match(TokenType.COUT.value)
    t.append(exp())
    match(TokenType.SEMMICOL.value)
    return t

def exp()->Tree:
    global token
    t = simp_exp()
    print("exp "+str(token))
    
    if( ( token == TokenType.LESSET.value ) or ( token == TokenType.LESST.value )  or
        ( token == TokenType.GREATERT.value ) or ( token == TokenType.GREATERET.value ) 
        or ( token == TokenType.EQ.value ) or (token == TokenType.DIFF.value)):
        p = Tree(tokenString,[])
        p.append(t)
     
        t = p
        match(token)
        t.append(simp_exp())
        
        
        
    return t        

def simp_exp()->Tree:
    global token 
    t = term()
    print("simp_exp")
    
    while( ( token == TokenType.PLUS.value) or ( token == TokenType.MINUS.value ) 
          or ( token == TokenType.PLUSP.value ) or ( token == TokenType.LESSL.value ) ):
        p = Tree(tokenString,[])
        p.append(t)
        t = p 
        match(token)
        p.append(term())
    return t

def term()->Tree:
    global token
    t = factor()
    print("term")
    
    while( (token == TokenType.TIMES.value) or (token==TokenType.OVER.value)or(token == TokenType.REMAINDER.value)):
        p = Tree(tokenString,[])
        p.append(t)
        t = p        
        match(token)
        p.append(factor())
        
    return t

def factor()->Tree:
    global token 
    global lineno
    t = Tree('',[])
    print("factor")
    
    global tokenString
    if ( token == TokenType.ENTERO.value ):
        t = Tree('Entero',[])
        t.append(Tree(tokenString,[]))
        match(TokenType.ENTERO.value)
    elif ( token == TokenType.NUMREAL.value ):
        t = Tree('Decimal',[])
        t.append(Tree(tokenString,[]))
        match(TokenType.NUMREAL.value)
    elif ( token == TokenType.ID.value ):
      
        t = Tree('Identificador',[])
        t.append(Tree(tokenString,[]))
        match(TokenType.ID.value)
    elif ( token == TokenType.LPAREN.value ):
        
         match(TokenType.LPAREN.value)
         t = exp()
         match(TokenType.RPAREN.value)
    else:
        print("unexpected token "+ str(token))
        sintaxError('Unexpected token -> '+tokenString)
        
        #printToken(token,tokenString)
        token = getTokenSintax()
    return t        
def parse()->Tree:
    global token
    global root
    global tokenString
    root = Tree('program',[])
    token = getTokenSintax()
    root.append(list_dec())
   
    if( token != TokenType.ENDFILE.value ):
        sintaxError(f'Code ends before file {token}\n')
    return root

def getTokenSintax():
    global source
    linea = source.readline()
    global tokenString
    global lineno
    global colpos
    if  linea:
        elementos = linea.split('\t')
        elementos = [elemento.replace("\n", "") for elemento in elementos]
        lts = []
        aux = elementos[0]
        if len(elementos)>=2:
            tokenString = elementos[1]
            lineno = elementos[2]
            colpos = elementos[3]
        if(elementos[0] == 'RESERVED-WORD'):
           aux = TokenType[elementos[1].upper()].value 
        else:
            aux = TokenType[aux.upper()].value 
        return aux   
    else:
        return TokenType.ENDFILE.value    


r = parse()
#print(r.pretty_print())
convert_to_json(r)
fileSintax.close()





""""

import tkinter as tk
from tkinter import ttk
from nltk import Tree

# Ejemplo de un árbol de NLTK
tree_nltk = Tree('S', [Tree('NP', ['John']), Tree('VP', ['sleeps'])])

window = tk.Tk()
window.title("Árbol de NLTK")

treeview = ttk.Treeview(window)
treeview["columns"] = ("Label", "Parent")
treeview.heading("#0", text="ID")
treeview.heading("Label", text="Label")
treeview.heading("Parent", text="Parent")

def add_tree_node(tree, parent_node=""):
    node_id = str(id(tree))  # Generar un identificador único para el nodo
    label = tree.label()
    treeview.insert(parent_node, tk.END, node_id, text=node_id, values=(label, parent_node))
    if isinstance(tree, Tree):
        for child in tree:
            add_tree_node(child, parent_node=node_id)

add_tree_node(r)

treeview.pack()
window.mainloop()"""







