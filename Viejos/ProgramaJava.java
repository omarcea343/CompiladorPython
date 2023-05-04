import java.io.*;

public class ProgramaJava {
    public static void main(String[] args) throws IOException {
        String texto1 = "Hola desde Java";
        String texto2 = "Otro texto desde Java";
        String[] command = { "python", "programa.py", texto1, texto2 };
        Runtime.getRuntime().exec(command);
    }
}