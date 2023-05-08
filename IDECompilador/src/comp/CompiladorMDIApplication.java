/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package comp;

import analizador.Token;
import java.awt.BorderLayout;
import java.awt.Color;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFileChooser;
import java.awt.Color;
import java.awt.Container;
import java.awt.Cursor;
import java.awt.Font;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.OutputStream;
import java.io.Reader;
import java.util.Arrays;
import javax.swing.JOptionPane;
import javax.swing.JTextPane;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableModel;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyleContext;

/**
 *
 * @author Javier
 */
public class CompiladorMDIApplication extends javax.swing.JFrame {

    /**
     * Creates new form CompiladorMDIApplication
     */
    File fnameContainer;
    String ruta = "";
    NumeroLinea numeroLinea;
    File file;
    DefaultTableModel modelo;

    public CompiladorMDIApplication() {
        initComponents();
        colors();
        Font fnt = new Font("Arial", Font.PLAIN, 15);
        Container con = getContentPane();
        con.setLayout(new BorderLayout());
        codigCompTextPane.setFont(fnt);
        numeroLinea = new NumeroLinea(codigCompTextPane);
        jScrollPane1.setRowHeaderView(numeroLinea);
        setTitle("Sin_titulo.txt");
        setVisible(true);
        modelo = new DefaultTableModel();
        modelo.addColumn("Clave");
        modelo.addColumn("Lexema");
        modelo.addColumn("Fila");
        modelo.addColumn("Columna");
        //modelo.addColumn("Fila");
        //modelo.addColumn("Columna");
        //tablaLexico.setModel(modelo);
    }

    //METODO PARA ENCONTRAR LAS ULTIMAS CADENAS
    private int findLastNonWordChar(String text, int index) {
        while (--index >= 0) {
            //  \\W = [A-Za-Z0-9]
            if (String.valueOf(text.charAt(index)).matches("\\W")) {
                break;
            }
        }
        return index;
    }

    //METODO PARA ENCONTRAR LAS PRIMERAS CADENAS 
    private int findFirstNonWordChar(String text, int index) {
        while (index < text.length()) {
            if (String.valueOf(text.charAt(index)).matches("\\W")) {
                break;
            }
            index++;
        }
        return index;
    }

    //METODO PARA PINTAS LAS PALABRAS RESEVADAS
    private void colors() {
        final StyleContext cont = StyleContext.getDefaultStyleContext();

        // Colores
        final AttributeSet attred = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(255, 0, 35));
        final AttributeSet attgreen = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(0, 255, 54));
        final AttributeSet attblue = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(0, 147, 255));
        final AttributeSet attblack = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(0, 0, 0));
        final AttributeSet attgray = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(128, 128, 128));

        // Estilo
        DefaultStyledDocument doc = new DefaultStyledDocument() {
            public void insertString(int offset, String str, AttributeSet a) throws BadLocationException {
                super.insertString(offset, str, (javax.swing.text.AttributeSet) a);
                applyStyles();
            }

            public void remove(int offs, int len) throws BadLocationException {
                super.remove(offs, len);
                applyStyles();
            }

            public void applyStyles() throws BadLocationException {
                String text = getText(0, getLength());

                int wordL = 0;
                int wordR = 0;

                while (wordR <= text.length()) {
                    if (wordR == text.length() || !Character.isLetterOrDigit(text.charAt(wordR))) {
                        if (wordR > wordL) {
                            String word = text.substring(wordL, wordR);
                            AttributeSet style = attblack;

                            if (word.matches("(\\W)*(main|if|then|else|end|do|while|repeat|until|cin|cout|real|int|boolean)")) {
                                style = attblue;
                            } else if (word.matches("(\\W)*\\d+(\\.\\d+)?")) {
                                style = attred;
                            }

                            setCharacterAttributes(wordL, wordR - wordL, style, false);
                        }
                        wordL = wordR;
                    }
                    wordR++;
                }

                // Buscar comentarios de una sola línea
                String[] lines = text.split("\n");
                for (String line : lines) {
                    if (line.trim().startsWith("//")) {
                        int lineStart = text.indexOf(line);
                        int lineEnd = lineStart + line.length();
                        setCharacterAttributes(lineStart, lineEnd - lineStart, attgray, false);
                    }
                }

                // Buscar comentarios multilinea
                int indexStart = text.indexOf("/*");
                int indexEnd = text.indexOf("*/");

                while (indexStart >= 0 && indexEnd >= 0 && indexEnd > indexStart) {
                    setCharacterAttributes(indexStart, indexEnd - indexStart + 2, attgray, false);

                    indexStart = text.indexOf("/*", indexEnd + 2);
                    indexEnd = text.indexOf("*/", indexEnd + 2);
                }
            }
        };

        JTextPane txt = new JTextPane(doc);
        String temp = codigCompTextPane.getText();
        codigCompTextPane.setStyledDocument(txt.getStyledDocument());
        codigCompTextPane.setText(temp);
    }

    public void SaveFile(String fname) throws IOException {
        setCursor(new Cursor(Cursor.WAIT_CURSOR));
        DataOutputStream o = new DataOutputStream(new FileOutputStream(fname));
        o.writeBytes(codigCompTextPane.getText());
        o.close();
        setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
    }

    public void OpenFile(String fname) throws IOException {
        //open file code here
        BufferedReader d = new BufferedReader(new InputStreamReader(new FileInputStream(fname)));
        String l;
        //clear the textbox
        codigCompTextPane.setText("");

        setCursor(new Cursor(Cursor.WAIT_CURSOR));

        while ((l = d.readLine()) != null) {
            codigCompTextPane.setText(codigCompTextPane.getText() + l + "\r\n");
        }

        setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
        d.close();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        desktopPane = new javax.swing.JDesktopPane();
        jPanel1 = new javax.swing.JPanel();
        titutloLabel = new javax.swing.JLabel();
        opcsTabbedPane = new javax.swing.JTabbedPane();
        lexicoPanel = new javax.swing.JPanel();
        btn_lex = new javax.swing.JButton();
        jScrollPane7 = new javax.swing.JScrollPane();
        lexicoTextPane = new javax.swing.JTextPane();
        sintacticoPanel = new javax.swing.JPanel();
        jScrollPane4 = new javax.swing.JScrollPane();
        SintacticoTextPane = new javax.swing.JTextPane();
        semanticoPanel = new javax.swing.JPanel();
        jScrollPane5 = new javax.swing.JScrollPane();
        SemanticoTextPane = new javax.swing.JTextPane();
        codigoIntermedioPanel = new javax.swing.JPanel();
        jScrollPane6 = new javax.swing.JScrollPane();
        CodIntermTextPane = new javax.swing.JTextPane();
        ErrResTabbedPane = new javax.swing.JTabbedPane();
        resultadosPanel = new javax.swing.JPanel();
        consolaTextPane = new javax.swing.JTextPane();
        erroresPanel = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        codigCompTextPane = new javax.swing.JTextPane();
        menuBar = new javax.swing.JMenuBar();
        archivoMenu = new javax.swing.JMenu();
        NuevoMenuItem = new javax.swing.JMenuItem();
        openMenuItem = new javax.swing.JMenuItem();
        saveMenuItem = new javax.swing.JMenuItem();
        saveAsMenuItem = new javax.swing.JMenuItem();
        exitMenuItem = new javax.swing.JMenuItem();
        editarMenu = new javax.swing.JMenu();
        cutMenuItem = new javax.swing.JMenuItem();
        copyMenuItem = new javax.swing.JMenuItem();
        pasteMenuItem = new javax.swing.JMenuItem();
        deleteMenuItem = new javax.swing.JMenuItem();
        formatoMenu = new javax.swing.JMenu();
        contentMenuItem = new javax.swing.JMenuItem();
        aboutMenuItem = new javax.swing.JMenuItem();
        compilarMenu = new javax.swing.JMenu();
        ayudaMenu = new javax.swing.JMenu();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        jPanel1.setBackground(new java.awt.Color(173, 36, 36));
        jPanel1.setMinimumSize(new java.awt.Dimension(800, 450));
        jPanel1.setPreferredSize(new java.awt.Dimension(500, 500));

        titutloLabel.setFont(new java.awt.Font("Book Antiqua", 0, 18)); // NOI18N
        titutloLabel.setForeground(new java.awt.Color(255, 255, 255));
        titutloLabel.setText("Código a Compilar");

        opcsTabbedPane.setFont(new java.awt.Font("Sitka Small", 0, 12)); // NOI18N

        btn_lex.setBackground(new java.awt.Color(51, 255, 51));
        btn_lex.setText("Léxico");
        btn_lex.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btn_lexActionPerformed(evt);
            }
        });

        lexicoTextPane.setEditable(false);
        lexicoTextPane.setFont(new java.awt.Font("Verdana", 0, 14)); // NOI18N
        jScrollPane7.setViewportView(lexicoTextPane);

        javax.swing.GroupLayout lexicoPanelLayout = new javax.swing.GroupLayout(lexicoPanel);
        lexicoPanel.setLayout(lexicoPanelLayout);
        lexicoPanelLayout.setHorizontalGroup(
            lexicoPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(btn_lex, javax.swing.GroupLayout.DEFAULT_SIZE, 465, Short.MAX_VALUE)
            .addGroup(lexicoPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane7)
                .addContainerGap())
        );
        lexicoPanelLayout.setVerticalGroup(
            lexicoPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(lexicoPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane7, javax.swing.GroupLayout.PREFERRED_SIZE, 471, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(btn_lex)
                .addContainerGap())
        );

        opcsTabbedPane.addTab("Léxico", lexicoPanel);

        jScrollPane4.setViewportView(SintacticoTextPane);

        javax.swing.GroupLayout sintacticoPanelLayout = new javax.swing.GroupLayout(sintacticoPanel);
        sintacticoPanel.setLayout(sintacticoPanelLayout);
        sintacticoPanelLayout.setHorizontalGroup(
            sintacticoPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane4, javax.swing.GroupLayout.DEFAULT_SIZE, 465, Short.MAX_VALUE)
        );
        sintacticoPanelLayout.setVerticalGroup(
            sintacticoPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane4, javax.swing.GroupLayout.DEFAULT_SIZE, 523, Short.MAX_VALUE)
        );

        opcsTabbedPane.addTab("Sintáctico", sintacticoPanel);

        jScrollPane5.setViewportView(SemanticoTextPane);

        javax.swing.GroupLayout semanticoPanelLayout = new javax.swing.GroupLayout(semanticoPanel);
        semanticoPanel.setLayout(semanticoPanelLayout);
        semanticoPanelLayout.setHorizontalGroup(
            semanticoPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane5, javax.swing.GroupLayout.DEFAULT_SIZE, 465, Short.MAX_VALUE)
        );
        semanticoPanelLayout.setVerticalGroup(
            semanticoPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane5, javax.swing.GroupLayout.DEFAULT_SIZE, 523, Short.MAX_VALUE)
        );

        opcsTabbedPane.addTab("Semántico", semanticoPanel);

        jScrollPane6.setViewportView(CodIntermTextPane);

        javax.swing.GroupLayout codigoIntermedioPanelLayout = new javax.swing.GroupLayout(codigoIntermedioPanel);
        codigoIntermedioPanel.setLayout(codigoIntermedioPanelLayout);
        codigoIntermedioPanelLayout.setHorizontalGroup(
            codigoIntermedioPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane6, javax.swing.GroupLayout.DEFAULT_SIZE, 465, Short.MAX_VALUE)
        );
        codigoIntermedioPanelLayout.setVerticalGroup(
            codigoIntermedioPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane6, javax.swing.GroupLayout.DEFAULT_SIZE, 523, Short.MAX_VALUE)
        );

        opcsTabbedPane.addTab("Código Intermedio", codigoIntermedioPanel);

        consolaTextPane.setEditable(false);

        javax.swing.GroupLayout resultadosPanelLayout = new javax.swing.GroupLayout(resultadosPanel);
        resultadosPanel.setLayout(resultadosPanelLayout);
        resultadosPanelLayout.setHorizontalGroup(
            resultadosPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(consolaTextPane, javax.swing.GroupLayout.DEFAULT_SIZE, 1115, Short.MAX_VALUE)
        );
        resultadosPanelLayout.setVerticalGroup(
            resultadosPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(resultadosPanelLayout.createSequentialGroup()
                .addGap(0, 1, Short.MAX_VALUE)
                .addComponent(consolaTextPane, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(0, 1, Short.MAX_VALUE))
        );

        ErrResTabbedPane.addTab("Resultados", resultadosPanel);

        javax.swing.GroupLayout erroresPanelLayout = new javax.swing.GroupLayout(erroresPanel);
        erroresPanel.setLayout(erroresPanelLayout);
        erroresPanelLayout.setHorizontalGroup(
            erroresPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 1115, Short.MAX_VALUE)
        );
        erroresPanelLayout.setVerticalGroup(
            erroresPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 87, Short.MAX_VALUE)
        );

        ErrResTabbedPane.addTab("Errores", erroresPanel);

        codigCompTextPane.setMaximumSize(new java.awt.Dimension(524, 583));
        jScrollPane1.setViewportView(codigCompTextPane);

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(23, 23, 23)
                        .addComponent(titutloLabel))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 583, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(opcsTabbedPane, javax.swing.GroupLayout.PREFERRED_SIZE, 470, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(62, 62, 62))
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(ErrResTabbedPane)
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addComponent(titutloLabel)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 524, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(opcsTabbedPane, javax.swing.GroupLayout.PREFERRED_SIZE, 553, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, Short.MAX_VALUE)
                .addComponent(ErrResTabbedPane, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(33, 33, 33))
        );

        desktopPane.add(jPanel1);
        jPanel1.setBounds(0, 0, 1140, 730);

        archivoMenu.setMnemonic('f');
        archivoMenu.setText("Archivo");

        NuevoMenuItem.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Iconos/icons8_code_file_48px.png"))); // NOI18N
        NuevoMenuItem.setText("Nuevo");
        NuevoMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                NuevoMenuItemActionPerformed(evt);
            }
        });
        archivoMenu.add(NuevoMenuItem);

        openMenuItem.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Iconos/icons8_opened_folder_48px.png"))); // NOI18N
        openMenuItem.setMnemonic('o');
        openMenuItem.setText("Abrir");
        openMenuItem.setMaximumSize(new java.awt.Dimension(500, 500));
        openMenuItem.setPreferredSize(new java.awt.Dimension(70, 54));
        openMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                openMenuItemActionPerformed(evt);
            }
        });
        archivoMenu.add(openMenuItem);

        saveMenuItem.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Iconos/icons8_save_48px.png"))); // NOI18N
        saveMenuItem.setMnemonic('s');
        saveMenuItem.setText("Guardar");
        saveMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                saveMenuItemActionPerformed(evt);
            }
        });
        archivoMenu.add(saveMenuItem);

        saveAsMenuItem.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Iconos/icons8_save_as_48px.png"))); // NOI18N
        saveAsMenuItem.setMnemonic('a');
        saveAsMenuItem.setText("Guardar Como");
        saveAsMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                saveAsMenuItemActionPerformed(evt);
            }
        });
        archivoMenu.add(saveAsMenuItem);

        exitMenuItem.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Iconos/icons-close.png"))); // NOI18N
        exitMenuItem.setMnemonic('x');
        exitMenuItem.setText("Cerrar");
        exitMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                exitMenuItemActionPerformed(evt);
            }
        });
        archivoMenu.add(exitMenuItem);

        menuBar.add(archivoMenu);

        editarMenu.setMnemonic('e');
        editarMenu.setText("Editar");

        cutMenuItem.setMnemonic('t');
        cutMenuItem.setText("Cut");
        editarMenu.add(cutMenuItem);

        copyMenuItem.setMnemonic('y');
        copyMenuItem.setText("Copy");
        editarMenu.add(copyMenuItem);

        pasteMenuItem.setMnemonic('p');
        pasteMenuItem.setText("Paste");
        editarMenu.add(pasteMenuItem);

        deleteMenuItem.setMnemonic('d');
        deleteMenuItem.setText("Delete");
        editarMenu.add(deleteMenuItem);

        menuBar.add(editarMenu);

        formatoMenu.setMnemonic('h');
        formatoMenu.setText("Formato");

        contentMenuItem.setMnemonic('c');
        contentMenuItem.setText("Contents");
        formatoMenu.add(contentMenuItem);

        aboutMenuItem.setMnemonic('a');
        aboutMenuItem.setText("About");
        formatoMenu.add(aboutMenuItem);

        menuBar.add(formatoMenu);

        compilarMenu.setText("Compilar");
        menuBar.add(compilarMenu);

        ayudaMenu.setText("Ayuda");
        menuBar.add(ayudaMenu);

        setJMenuBar(menuBar);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(desktopPane, javax.swing.GroupLayout.DEFAULT_SIZE, 1138, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(desktopPane, javax.swing.GroupLayout.DEFAULT_SIZE, 726, Short.MAX_VALUE)
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void openMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_openMenuItemActionPerformed
        // TODO add your handling code here:
        /*JFileChooser buscador = new JFileChooser();
         buscador.showOpenDialog(buscador);
        
         //Método que devuelve la ruta de acceso
         String patch = buscador.getSelectedFile().getAbsolutePath();
         try {
         //Abrir archivo
         FileInputStream archivo = new FileInputStream(patch);
         //Crear objeto de entrada
         DataInputStream entrada = new DataInputStream(archivo);
         // crear buffer de lectura
         BufferedReader buffer = new BufferedReader(new InputStreamReader(entrada));
        
         String lineas, res = "";
            
         while((lineas = buffer.readLine()) != null){
         res = res + lineas + "\n";
         }
         if(!"".equals(res)){
         consolaTextPane.setText(consolaTextPane.getText()+"\nAVISO: Archivo cargado correctamente.");
         }else{
         consolaTextPane.setText(consolaTextPane.getText()+"\nAVISO: No hay texto para cargar.");
         }
         codigCompTextPane.setText(res);
         } catch (FileNotFoundException ex) {
         Logger.getLogger(CompiladorMDIApplication.class.getName()).log(Level.SEVERE, null, ex);
         } catch (IOException ex) {
         Logger.getLogger(CompiladorMDIApplication.class.getName()).log(Level.SEVERE, null, ex);
         }*/
        JFileChooser jfc = new JFileChooser();

        FileNameExtensionFilter filter = new FileNameExtensionFilter("Archivos de texto", "txt");
        jfc.setFileFilter(filter);

        int ret = jfc.showDialog(null, "Abrir");

        if (ret == JFileChooser.APPROVE_OPTION) {
            try {
                File fyl = jfc.getSelectedFile();
                ruta = fyl.getAbsolutePath();
                OpenFile(fyl.getAbsolutePath());
                this.setTitle(fyl.getName());
                fnameContainer = fyl;
                consolaTextPane.setText(consolaTextPane.getText() + "\nAVISO: Archivo cargado correctamente.");

            } catch (IOException ers) {
            }

        }

    }//GEN-LAST:event_openMenuItemActionPerformed

    private void NuevoMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NuevoMenuItemActionPerformed
        // TODO add your handling code here:
        this.setTitle("Sin_titulo.txt");
        codigCompTextPane.setText("");
        fnameContainer = null;
        ruta = "";
        for (int i = 0; i < modelo.getRowCount(); i++) {
            modelo.removeRow(i);
            i -= 1;
        }
    }//GEN-LAST:event_NuevoMenuItemActionPerformed

    private void saveMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_saveMenuItemActionPerformed
        // TODO add your handling code here:
        if (getTitle().equals("Sin_titulo.txt")) {

            JFileChooser jfc = new JFileChooser();
            if (fnameContainer != null) {
                jfc.setCurrentDirectory(fnameContainer);
                jfc.setSelectedFile(fnameContainer);
            } else {
                jfc.setSelectedFile(new File("Sin_titulo.txt"));
            }

            int ret = jfc.showSaveDialog(null);

            if (ret == JFileChooser.APPROVE_OPTION) {
                try {
                    File fyl = jfc.getSelectedFile();
                    SaveFile(fyl.getAbsolutePath());
                    System.out.println(fyl.getAbsolutePath());
                    ruta = fyl.getAbsolutePath();
                    this.setTitle(fyl.getName());
                    fnameContainer = fyl;
                    JOptionPane.showMessageDialog(null, "Operación completada con éxito", "Mensaje de información", JOptionPane.INFORMATION_MESSAGE);
                    consolaTextPane.setText(consolaTextPane.getText() + "\nAVISO: Archivo creado y guardado exitosamente.");

                } catch (Exception ers2) {
                }
            }
        } else {
            File archivo = new File(ruta);
            try {
                FileWriter writer = new FileWriter(archivo, false);
                writer.write(codigCompTextPane.getText());
                writer.close();
                JOptionPane.showMessageDialog(null, "Operación completada con éxito", "Guardar", JOptionPane.INFORMATION_MESSAGE);
                consolaTextPane.setText(consolaTextPane.getText() + "\nAVISO: Cambios aplicados exitosamente.");
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }

    }//GEN-LAST:event_saveMenuItemActionPerformed

    private void saveAsMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_saveAsMenuItemActionPerformed
        // TODO add your handling code here:
        if (getTitle().equals("Sin_titulo.txt")) {
            JOptionPane.showMessageDialog(null, "Ningún archivo ha sido seleccionado...");
        } else {

            JFileChooser jfc = new JFileChooser();
            if (fnameContainer != null) {
                jfc.setCurrentDirectory(fnameContainer);
                jfc.setSelectedFile(fnameContainer);
            } else {
                //jfc.setCurrentDirectory(new File("."));
                jfc.setSelectedFile(new File("Sin_titulo.txt"));
            }

            int ret = jfc.showSaveDialog(null);

            if (ret == JFileChooser.APPROVE_OPTION) {
                try {
                    File fyl = jfc.getSelectedFile();
                    SaveFile(fyl.getAbsolutePath());
                    this.setTitle(fyl.getName());
                    fnameContainer = fyl;

                } catch (Exception ers2) {
                }
            }
        }

    }//GEN-LAST:event_saveAsMenuItemActionPerformed

    private void exitMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_exitMenuItemActionPerformed
        if (this.getTitle().equals("Sin_titulo.txt")) {
            JOptionPane.showMessageDialog(null, "Ningún Archivo está abierto", "Cerrar Archivo", JOptionPane.ERROR_MESSAGE);
        } else {
            FileInputStream inputStream = null;
            try {
                inputStream = new FileInputStream(ruta);
                // Operaciones necesarias sobre el archivo
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    if (inputStream != null) {
                        inputStream.close();
                        this.setTitle("Sin_titulo.txt");
                        codigCompTextPane.setText("");
                        fnameContainer = null;
                        ruta = "";
                        for (int i = 0; i < modelo.getRowCount(); i++) {
                            modelo.removeRow(i);
                            i -= 1;
                        }
                        consolaTextPane.setText(consolaTextPane.getText() + "\nAVISO: Archivo cerrado correctamente.");
                        JOptionPane.showMessageDialog(null, "Archivo Cerrado Correctamente", "Cerrar Archivo", JOptionPane.INFORMATION_MESSAGE);

                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }//GEN-LAST:event_exitMenuItemActionPerformed

    private void btn_lexActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btn_lexActionPerformed
        System.out.println("HOLA " + this.ruta);

        if (this.ruta.equals("") && codigCompTextPane.getText().equals("")) {
            JOptionPane.showMessageDialog(null, "Ningún archivo", "Seleccione algún archivo", JOptionPane.ERROR_MESSAGE);
        } else if (!codigCompTextPane.getText().equals("") && this.ruta.equals("") && this.getTitle().equals("Sin_titulo.txt")) {

            JFileChooser jfc = new JFileChooser();
            if (fnameContainer != null) {
                jfc.setCurrentDirectory(fnameContainer);
                jfc.setSelectedFile(fnameContainer);
            } else {
                jfc.setSelectedFile(new File("Sin_titulo.txt"));
            }

            int ret = jfc.showSaveDialog(null);

            if (ret == JFileChooser.APPROVE_OPTION) {
                try {
                    File fyl = jfc.getSelectedFile();
                    SaveFile(fyl.getAbsolutePath());
                    System.out.println(fyl.getAbsolutePath());
                    ruta = fyl.getAbsolutePath();
                    this.setTitle(fyl.getName());
                    fnameContainer = fyl;
                    JOptionPane.showMessageDialog(null, "Operación completada con éxito", "Mensaje de información", JOptionPane.INFORMATION_MESSAGE);
                    consolaTextPane.setText(consolaTextPane.getText() + "\nAVISO: Archivo creado y guardado exitosamente.");
                    // Ruta al script de Python
                    String scriptPath = "C:/Users/Omar/Desktop/Compilador/Compilador/src/comp/lexico.py";

                    // Argumentos que se pasarán al script
                    String[] scriptArgs = new String[]{ruta};

                    // Crea el proceso para ejecutar el script
                    ProcessBuilder pb = new ProcessBuilder("python", scriptPath);
                    pb.redirectErrorStream(true);

                    // Agrega los argumentos al proceso
                    pb.command().addAll(Arrays.asList(scriptArgs));

                    // Ejecuta el proceso y espera a que termine
                    Process process = null;
                    try {
                        process = pb.start();
                    } catch (IOException ex) {
                        Logger.getLogger(CompiladorMDIApplication.class.getName()).log(Level.SEVERE, null, ex);
                    }
                    try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            System.out.println(line);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                    String rutaArchivo = "ResultadosLexico.txt";

                    // Se usa un try-with-resources para asegurarse de que el archivo se cierre correctamente
                    try (BufferedReader br = new BufferedReader(new FileReader(rutaArchivo))) {

                        String contenidoArchivo = "";
                        String lineaActual;

                        // Se lee el archivo línea por línea y se almacena el contenido en una variable
                        while ((lineaActual = br.readLine()) != null) {
                            contenidoArchivo += lineaActual + "\n";
                        }

                        // Se obtiene el JTextPane y se establece su contenido con el contenido del archivo
                        lexicoTextPane.setText(contenidoArchivo);

                    } catch (IOException e) {
                        System.err.println("Error al leer el archivo: " + e.getMessage());
                    }
                } catch (Exception ers2) {
                }
            }
        } else if (!codigCompTextPane.getText().equals("") && !this.ruta.equals("") && !this.getTitle().equals("Sin_titulo.txt")) {
            ruta = ruta;
            // Ruta al script de Python
            String scriptPath = "C:/Users/Omar/Desktop/Compilador/Compilador/src/comp/lexico.py";

            // Argumentos que se pasarán al script
            String[] scriptArgs = new String[]{ruta};

            // Crea el proceso para ejecutar el script
            ProcessBuilder pb = new ProcessBuilder("python", scriptPath);
            pb.redirectErrorStream(true);

            // Agrega los argumentos al proceso
            pb.command().addAll(Arrays.asList(scriptArgs));

            // Ejecuta el proceso y espera a que termine
            Process process = null;
            try {
                process = pb.start();
            } catch (IOException ex) {
                Logger.getLogger(CompiladorMDIApplication.class.getName()).log(Level.SEVERE, null, ex);
            }
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            String rutaArchivo = "ResultadosLexico.txt";

            // Se usa un try-with-resources para asegurarse de que el archivo se cierre correctamente
            try (BufferedReader br = new BufferedReader(new FileReader(rutaArchivo))) {

                String contenidoArchivo = "";
                String lineaActual;

                // Se lee el archivo línea por línea y se almacena el contenido en una variable
                while ((lineaActual = br.readLine()) != null) {
                    contenidoArchivo += lineaActual + "\n";
                }

                // Se obtiene el JTextPane y se establece su contenido con el contenido del archivo
                lexicoTextPane.setText(contenidoArchivo);

            } catch (IOException e) {
                System.err.println("Error al leer el archivo: " + e.getMessage());
            }
        }

        /*for (int i = 0; i < tablaLexico.getRowCount(); i++) {
         modelo.removeRow(i);
         i -= 1;
            
         }
         if (fnameContainer == null) {
         JOptionPane.showMessageDialog(null, "Ningún Archivo ha sido cargado", "Archivo", JOptionPane.INFORMATION_MESSAGE);
         } else {
         consolaTextPane.setText(consolaTextPane.getText() + "\nAVISO: Análisis Léxico llevado a cabo correctamente.");

         try {
         Reader lector = new BufferedReader(new FileReader(fnameContainer));
         Lexer lexer = new Lexer(lector);
         String resultado = "";
         String[] Datos = new String[4];
         while (true) {
         Token tokens = lexer.yylex();
         if (tokens == null) {
         resultado += "FIN";
         return;
         }
         switch (tokens) {
         case ERROR:
         resultado += "Simbolo no definido\n";
         break;
         case Identificador:
         Datos[0] = "ID";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Numero:
         Datos[0] = "NUM";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Reservadas:
         Datos[0] = "RESERV";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
            
         break;
         case Suma:
         Datos[0] = "SUM";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Resta:
         Datos[0] = "REST";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Multiplicacion:
         Datos[0] = "MULT";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Division:
         Datos[0] = "DIVI";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Potencia:
         Datos[0] = "POTE";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Menor:
         Datos[0] = "MEN";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case MenorIgual:
         Datos[0] = "MENIG";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Mayor:
         Datos[0] = "MAY";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case MayorIgual:
         Datos[0] = "MAYIG";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case IgualIgual:
         Datos[0] = "IGIG";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Diferente:
         Datos[0] = "DIF";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Igual:
         Datos[0] = "IG";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case PuntoComa:
         Datos[0] = "PUNTCOM";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case Coma:
         Datos[0] = "COM";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case ParAb:
         Datos[0] = "PA";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case ParCi:
         Datos[0] = "PC";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         resultado += lexer.lexeme + " es un " + tokens;
         break;
         case LlaAb:
         Datos[0] = "LLAAB";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         case LlaCi:
         Datos[0] = "LLACI";
         Datos[1] = lexer.lexeme;
         Datos[2] = Integer.toString(lexer.fila);
         Datos[3] = Integer.toString(lexer.columna);
         modelo.addRow(Datos);
         break;
         default:
         resultado += "Token: " + tokens + "\n";
         break;
         }
         }
            
         } catch (FileNotFoundException ex) {
         Logger.getLogger(CompiladorMDIApplication.class.getName()).log(Level.SEVERE, null, ex);
         } catch (IOException ex) {
         Logger.getLogger(CompiladorMDIApplication.class.getName()).log(Level.SEVERE, null, ex);
         }
         }*/

    }//GEN-LAST:event_btn_lexActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */

        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(CompiladorMDIApplication.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(CompiladorMDIApplication.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(CompiladorMDIApplication.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(CompiladorMDIApplication.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new CompiladorMDIApplication().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JTextPane CodIntermTextPane;
    private javax.swing.JTabbedPane ErrResTabbedPane;
    private javax.swing.JMenuItem NuevoMenuItem;
    private javax.swing.JTextPane SemanticoTextPane;
    private javax.swing.JTextPane SintacticoTextPane;
    private javax.swing.JMenuItem aboutMenuItem;
    private javax.swing.JMenu archivoMenu;
    private javax.swing.JMenu ayudaMenu;
    private javax.swing.JButton btn_lex;
    private javax.swing.JTextPane codigCompTextPane;
    private javax.swing.JPanel codigoIntermedioPanel;
    private javax.swing.JMenu compilarMenu;
    private javax.swing.JTextPane consolaTextPane;
    private javax.swing.JMenuItem contentMenuItem;
    private javax.swing.JMenuItem copyMenuItem;
    private javax.swing.JMenuItem cutMenuItem;
    private javax.swing.JMenuItem deleteMenuItem;
    private javax.swing.JDesktopPane desktopPane;
    private javax.swing.JMenu editarMenu;
    private javax.swing.JPanel erroresPanel;
    private javax.swing.JMenuItem exitMenuItem;
    private javax.swing.JMenu formatoMenu;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane4;
    private javax.swing.JScrollPane jScrollPane5;
    private javax.swing.JScrollPane jScrollPane6;
    private javax.swing.JScrollPane jScrollPane7;
    private javax.swing.JPanel lexicoPanel;
    private javax.swing.JTextPane lexicoTextPane;
    private javax.swing.JMenuBar menuBar;
    private javax.swing.JTabbedPane opcsTabbedPane;
    private javax.swing.JMenuItem openMenuItem;
    private javax.swing.JMenuItem pasteMenuItem;
    private javax.swing.JPanel resultadosPanel;
    private javax.swing.JMenuItem saveAsMenuItem;
    private javax.swing.JMenuItem saveMenuItem;
    private javax.swing.JPanel semanticoPanel;
    private javax.swing.JPanel sintacticoPanel;
    private javax.swing.JLabel titutloLabel;
    // End of variables declaration//GEN-END:variables

}
