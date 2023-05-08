package analizador;
import static analizador.Token.*;
%%
%class Lexer
%line
%column
%type Token
L=[a-zA-Z_]+
D=[0-9]+
espacio=[ ,\t,\r,\n]+
%{
    public String lexeme;
    public int columna;
    public int fila;
%}
%%
program |
if |
else |
fi |
do |
until |
while |
read | 
write |
float |
int |
bool |
not |
and |
or |
public |
static |
void |
main |
while {lexeme=yytext(); columna=yycolumn;fila=yyline;return Reservadas;}
{espacio} {/*Ignore*/}
"//".* {/*Ignore*/}
"=" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Igual;}
"+" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Suma;}
"-" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Resta;}
"*" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Multiplicacion;}
"/" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Division;}
"^" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Potencia;}
"<" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Menor;}
"<=" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return MenorIgual;}
">" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Mayor;}
">=" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return MayorIgual;}
"==" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return IgualIgual;}
"!=" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Diferente;}
";" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return PuntoComa;}
"," {lexeme=yytext();columna=yycolumn;fila=yyline+1;return Coma;}
"(" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return ParAb;}
")" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return ParCi;}
"{" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return LlaAb;}
"}" {lexeme=yytext();columna=yycolumn;fila=yyline+1;return LlaCi;}
{L}({L}|{D})* {lexeme=yytext(); columna=yycolumn;fila=yyline+1;return Identificador;}
{D} {D}* (.{D}D*)? {lexeme=yytext(); columna=yycolumn;fila=yyline+1;return Numero;}
 . {return ERROR;}
