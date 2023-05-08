/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package analizador;

import java.io.File;

/**
 *
 * @author Javier
 */
public class JFlexNetBeans {

    public static void main(String[] args) {
        String rutaLexer = "C:/Users/Javier/Documents/NetBeansProjects/Compilador/src/analizador/Lexer.flex";
        generarJavaLexer(rutaLexer);
    }
    
    public static void generarJavaLexer(String rutaLexer){
        File archivo = new File(rutaLexer);
        jflex.Main.generate(archivo);
    }
}
