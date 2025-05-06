from tkinter import Tk, Menu, PhotoImage, Entry, Text, PanedWindow, Frame, Scrollbar, BOTH, VERTICAL, HORIZONTAL, END, WORD, RAISED
from os import path
from tabulate import tabulate
import re
from analizador_semantico.analizador_semantico import AnalizadorSemanticoR


directorio_actual = path.dirname(__file__) 

class Ventana:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Compilador lenguaje R")
        self.ventana.geometry("1000x700")  # Increased window size for better usability

        # Definir colores para la interfaz
        self.colors = {
            "bg_main": "#f0f0f0",
            "bg_editor": "#282c34",
            "fg_editor": "#abb2bf",
            "bg_output": "#21252b",
            "fg_output": "#d7dae0",
            "keyword": "#c678dd",
            "operator": "#56b6c2",
            "number": "#d19a66",
            "string": "#98c379",
            "comment": "#7f848e",
            "identifier": "#e5c07b",
            "delimiter": "#61afef",
            "error": "#e06c75"
        }

        # Configurar tema de la ventana
        self.ventana.configure(bg=self.colors["bg_main"])

        #iconos utilizados en el menu superior
        self.save_icon = PhotoImage(file=directorio_actual + "/assets/menu_archivo/save.png").subsample(2, 2)
        self.clean_icon = PhotoImage(file=directorio_actual + "/assets/menu_archivo/clean.png").subsample(2, 2)
        self.close_icon = PhotoImage(file=directorio_actual + "/assets/menu_archivo/close.png").subsample(2, 2)
        self.exit_icon = PhotoImage(file=directorio_actual + "/assets/menu_archivo/exit.png").subsample(2, 2)
        self.lexico_icon = PhotoImage(file=directorio_actual + "/assets/menu_compiladores/lexico.png").subsample(2, 2)
        self.sintactico_icon = PhotoImage(file=directorio_actual + "/assets/menu_compiladores/sintactico.png").subsample(2, 2)
        self.semantico_icon = PhotoImage(file=directorio_actual + "/assets/menu_compiladores/semantico.png").subsample(2, 2)
        self.generar_codigo= PhotoImage(file=directorio_actual + "/assets/menu_compiladores/generar.png").subsample(2, 2)
        self.objeto =  PhotoImage(file=directorio_actual + "/assets/menu_compiladores/objeto.png").subsample(2, 2)
        self.int_icon = PhotoImage(file=directorio_actual + "/assets/menu_variables/int.png").subsample(2, 2)
        self.float_icon = PhotoImage(file=directorio_actual + "/assets/menu_variables/float.png").subsample(2, 2)
        self.char_icon = PhotoImage(file=directorio_actual + "/assets/menu_variables/char.png").subsample(2, 2)
        self.double_icon = PhotoImage(file=directorio_actual + "/assets/menu_variables/double.png").subsample(2, 2)

        # Patrones para resaltado de sintaxis
        self.syntax_patterns = {
            'keyword': r'\b(if|else|while|for|function|return|break|next|switch|TRUE|FALSE|NULL|NA|Inf|NaN|print|in|repeat)\b',
            'operator': r'(<-|<<-|->|=|\+|-|\*|/|%|^|&|\||!|>=|<=|==|!=|<|>)',
            'number': r'\b\d*\.\d+|\d+\b',
            'string': r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'',
            'comment': r'#.*',
            'delimiter': r'[\(\)\{\}\[\],;]',
        }

        self.menuSuperior()
        self.compilador = AnalizadorSemanticoR()
        self.editores()

        # Aplicar resaltado de sintaxis inicial
        self.ventana.after(100, self.highlight_syntax)

    def menu_archivo(self):

        menu_archivo = Menu(self.menu, tearoff=0)
        menu_archivo.add_command(label="Guardar", accelerator="Ctrl+G", image=self.save_icon, compound="left")
        menu_archivo.add_command(label="Limpiar pantalla", accelerator="Ctrl+L", image=self.clean_icon, compound="left", command=self.limpiar_pantalla)
        menu_archivo.add_command(label="Cerrar", accelerator="Ctrl+W",  image=self.close_icon, compound="left")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.quit, accelerator="Ctrl+Q", image=self.exit_icon, compound="left")

        return menu_archivo
    def menu_editar(self):

        menu_archivo = Menu(self.menu, tearoff=0)

        return menu_archivo
    def menu_ejectuar(self):

        menu_ejecutar = Menu(self.menu, tearoff=0)

        return menu_ejecutar
    def menu_compiladores(self):
        menu_compiladores = Menu(self.menu, tearoff=0)
        menu_compiladores.add_command(label="Analizador Léxico", accelerator="Alt+L", image=self.lexico_icon, compound="left", command=self.analizar_lexico)
        menu_compiladores.add_command(label="Analizador Sintáctico", accelerator="Alt+S", image=self.sintactico_icon, compound="left",  command=self.analizar_sintactico)
        menu_compiladores.add_command(label="Analizador Semántico", accelerator="Alt+M", image=self.semantico_icon, compound="left", command=self.analizar_semantico)
        menu_compiladores.add_command(label="Generador de Código", accelerator= "Alt+G", image=self.generar_codigo, compound="left")
        menu_compiladores.add_command(label="Codigo Objeto", accelerator="Alt+C", image=self.objeto, compound="left")

        return menu_compiladores
    def menu_ayuda(self):
        #TODO: actualizar con libreria de R
        menu_ayuda = Menu(self.menu, tearoff=0)
        submenu_librerias = Menu(menu_ayuda, tearoff=0)
        menu_ayuda.add_cascade(label="Librerías", menu=submenu_librerias)
        submenu_librerias.add_command(label="stdio.h")
        submenu_librerias.add_command(label="conio.h")
        submenu_librerias.add_command(label="math.h")
        submenu_librerias.add_command(label="string.h")
        submenu_librerias.add_command(label="stdlib.h")
        submenu_librerias.add_command(label="ctype.h")
        submenu_variables = Menu(menu_ayuda, tearoff=0)
        # depois
        return menu_ayuda
    def menu_variables(self):
        menu_variables = Menu(self.menu, tearoff=0)
        menu_tipos = Menu(menu_variables, tearoff=0)
        menu_variables.add_cascade(label="Tipos", menu=menu_tipos)
        menu_tipos.add_command(label="int", image=self.int_icon, compound='left')
        menu_tipos.add_command(label="float", image=self.float_icon, compound='left')
        menu_tipos.add_command(label="char", image=self.char_icon, compound='left')
        menu_tipos.add_command(label="double", image=self.double_icon, compound='left')
        return menu_variables
    def caja_texto_entrada(self):
        entrada = Entry(self.ventana, width=30)
        entrada.insert(0, "Texto por defecto")
        return entrada
    def menuSuperior(self):
        self.menu = Menu(self.ventana)
        # Menú específico para macOS
        if self.ventana.tk.call('tk', 'windowingsystem') == 'aqua': # macOS
            appmenu = Menu(self.menu, name='apple')
            self.menu.add_cascade(menu=appmenu)  # Esto hace que aparezca en macOS       
            self.ventana.config(menu=self.menu)
        else:
            appmenu = self.menu
        # Menú Archivo
        menu_archivo = self.menu_archivo()
        # Menú Editar   
        menu_editar = self.menu_editar()
        #menu Ejecutar
        menu_ejecutar = self.menu_ejectuar()
        #menu Compiladores
        menu_compiladores = self.menu_compiladores()
        # Menú Ayuda
        menu_ayuda = self.menu_ayuda()
        #meu variables
        menu_variables = self.menu_variables()
        # Agregar al menú principal
        self.menu.add_cascade(label="Archivo", menu=menu_archivo)
        self.menu.add_cascade(label="Editar", menu=menu_editar)
        self.menu.add_cascade(label="Ejecutar", menu=menu_ejecutar)
        self.menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        self.menu.add_cascade(label="Compiladores", menu=menu_compiladores)
        self.menu.add_cascade(label="Variables", menu=menu_variables)
        # caja de texto
        self.ventana.config(menu=self.menu)

    def highlight_syntax(self, event=None):
        """
        Aplica resaltado de sintaxis al editor de código
        """
        # Eliminar todas las etiquetas existentes
        for tag in self.editor.tag_names():
            self.editor.tag_remove(tag, "1.0", "end")

        # Obtener el texto completo
        content = self.editor.get("1.0", "end-1c")

        # Aplicar resaltado para cada patrón
        for pattern_name, pattern in self.syntax_patterns.items():
            self.editor.tag_configure(pattern_name, foreground=self.colors[pattern_name])

            # Buscar todas las coincidencias del patrón
            for match in re.finditer(pattern, content):
                start_index = "1.0 + {} chars".format(match.start())
                end_index = "1.0 + {} chars".format(match.end())
                self.editor.tag_add(pattern_name, start_index, end_index)

        # Resaltar identificadores (todo lo que no coincida con otros patrones)
        self.editor.tag_configure("identifier", foreground=self.colors["identifier"])

        return "break"  # Evitar comportamiento predeterminado

    def actualizar_numeros_linea(self, event=None):
        """
        Actualiza los números de línea en el editor
        """
        if not hasattr(self, 'line_numbers'):
            return

        # Obtener todas las líneas del editor
        lineas = self.editor.get('1.0', 'end-1c').split('\n')
        line_count = len(lineas)

        # Actualizar números de línea
        self.line_numbers.configure(state='normal')
        self.line_numbers.delete('1.0', 'end')

        for i in range(1, line_count + 1):
            self.line_numbers.insert('end', f"{i}\n")

        self.line_numbers.configure(state='disabled')

    def editores(self):
        """
        Crea los editores de código y salida con diseño flexible
        """
        # Crear un PanedWindow para dividir la ventana en secciones redimensionables
        self.paned = PanedWindow(self.ventana, orient='vertical', sashrelief=RAISED, sashwidth=4)
        self.paned.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Frame para el editor de código
        editor_frame = Frame(self.paned, bg=self.colors["bg_main"])

        # Crear widget para números de línea
        self.line_numbers = Text(editor_frame, width=4, padx=3, pady=5, takefocus=0, 
                                 bg=self.colors["bg_editor"], fg="#636d83", 
                                 border=0, highlightthickness=0)
        self.line_numbers.pack(side='left', fill='y')
        self.line_numbers.configure(state='disabled')

        # Crear caja de texto principal para el código con scrollbars
        self.editor = Text(editor_frame, wrap=WORD, undo=True, maxundo=-1)
        editor_scrolly = Scrollbar(editor_frame, orient=VERTICAL, command=self.editor.yview)
        editor_scrollx = Scrollbar(editor_frame, orient=HORIZONTAL, command=self.editor.xview)
        self.editor.configure(yscrollcommand=editor_scrolly.set, xscrollcommand=editor_scrollx.set)

        # Posicionar elementos del editor
        editor_scrolly.pack(side='right', fill='y')
        editor_scrollx.pack(side='bottom', fill='x')
        self.editor.pack(side='left', fill='both', expand=True)

        # Frame para la salida
        output_frame = Frame(self.paned, bg=self.colors["bg_main"])

        # Crear caja de texto para la salida/resultados con scrollbars
        self.output = Text(output_frame, state='disabled', wrap=WORD)
        output_scrolly = Scrollbar(output_frame, orient=VERTICAL, command=self.output.yview)
        output_scrollx = Scrollbar(output_frame, orient=HORIZONTAL, command=self.output.xview)
        self.output.configure(yscrollcommand=output_scrolly.set, xscrollcommand=output_scrollx.set)

        # Posicionar elementos de la salida
        output_scrolly.pack(side='right', fill='y')
        output_scrollx.pack(side='bottom', fill='x')
        self.output.pack(side='left', fill='both', expand=True)

        # Añadir frames al PanedWindow
        self.paned.add(editor_frame, height=500)  # Editor más grande
        self.paned.add(output_frame, height=200)  # Salida más pequeña

        # Configurar colores y fuentes
        self.editor.configure(
            bg=self.colors["bg_editor"], 
            fg=self.colors["fg_editor"], 
            font=('Consolas', 12),
            insertbackground=self.colors["fg_editor"],  # Color del cursor
            selectbackground="#3e4451",  # Color de selección
            selectforeground=self.colors["fg_editor"],
            padx=5, pady=5
        )

        self.output.configure(
            bg=self.colors["bg_output"], 
            fg=self.colors["fg_output"], 
            font=('Consolas', 12),
            padx=5, pady=5
        )

        # Función combinada para manejar eventos de edición
        def on_editor_change(event):
            self.highlight_syntax()
            self.actualizar_numeros_linea()
            return "break"

        # Configurar eventos para resaltado de sintaxis y números de línea
        self.editor.bind("<KeyRelease>", on_editor_change)
        self.editor.bind("<FocusIn>", self.highlight_syntax)
        self.editor.bind("<<Change>>", self.actualizar_numeros_linea)
        self.editor.bind("<Configure>", self.actualizar_numeros_linea)
        self.editor.bind("<MouseWheel>", self.actualizar_numeros_linea)

        # Sincronizar scroll de números de línea con editor
        def on_editor_scroll(*args):
            self.line_numbers.yview_moveto(args[0])
        self.editor.vbar = editor_scrolly
        self.editor.vbar.bind("<Motion>", lambda e: on_editor_scroll(self.editor.yview()[0]))

        # Configurar atajos de teclado
        self.ventana.bind("<Control-l>", lambda event: self.limpiar_pantalla())
        self.ventana.bind("<Alt-l>", lambda event: self.analizar_lexico())
        self.ventana.bind("<Alt-s>", lambda event: self.analizar_sintactico())
        self.ventana.bind("<Alt-m>", lambda event: self.analizar_semantico())

        # Inicializar números de línea
        self.actualizar_numeros_linea()

    def output_texto(self, texto):
        """
        Módulo para imprimir texto en la salida del texto
        :param texto: El texto que se mostrará en la caja de salida
        :return: None
        """
        self.output.configure(state='normal')

        # Limpiar contenido anterior
        self.output.delete('1.0', 'end')

        # Insertar nuevo texto con formato
        self.output.insert('end', texto + '\n')

        # Aplicar colores a secciones específicas
        content = self.output.get('1.0', 'end-1c')

        # Resaltar títulos de secciones
        title_pattern = r'ANALISIS (LEXICO|SINTACTICO|SEMANTICO)'
        for match in re.finditer(title_pattern, content):
            start_index = "1.0 + {} chars".format(match.start())
            end_index = "1.0 + {} chars".format(match.end())
            self.output.tag_add("title", start_index, end_index)

        # Resaltar errores
        error_pattern = r'Error.*'
        for match in re.finditer(error_pattern, content):
            start_index = "1.0 + {} chars".format(match.start())
            end_index = "1.0 + {} chars".format(match.end())
            self.output.tag_add("error_msg", start_index, end_index)

        # Configurar estilos de etiquetas
        self.output.tag_configure("title", foreground="#61afef", font=('Consolas', 14, 'bold'))
        self.output.tag_configure("error_msg", foreground=self.colors["error"])

        self.output.see('end')
        self.output.configure(state='disabled')

    def limpiar_pantalla(self):
        """
        Limpia el contenido del editor y la salida
        """
        # Limpiar editor
        self.editor.delete("1.0", "end")

        # Limpiar salida
        self.output.configure(state='normal')
        self.output.delete("1.0", "end")
        self.output.configure(state='disabled')

        # Actualizar resaltado de sintaxis y números de línea
        self.highlight_syntax()
        self.actualizar_numeros_linea()

    def obtener_input(self):
        return self.editor.get("1.0", "end-1c")
    def analizar_sintactico(self):
        self.compilador.analizador_sintactico.analizar(self.obtener_input())

        texto = "ANALISIS SINTACTICO \n"
        texto += "-" * 20 + "\n"
        texto += tabulate( self.compilador.analizador_sintactico.tokens, headers="keys", tablefmt="grid")
        texto += "\n"
        texto += "Errores Encontrados"
        texto += tabulate( self.compilador.analizador_sintactico.errores, headers="keys", tablefmt="grid")
        self.output_texto(texto)

    def analizar_lexico(self):
        self.compilador.analizador_sintactico.analizador_lexico.analizar(self.obtener_input())

        texto = "ANALISIS LEXICO \n"
        texto += "-" * 20 + "\n"
        texto += tabulate( self.compilador.analizador_sintactico.analizador_lexico.tokens, headers="keys", tablefmt="grid")
        texto += "\n"
        texto += "Errores Encontrados\n"
        texto += tabulate( self.compilador.analizador_sintactico.analizador_lexico.errores, headers="keys", tablefmt="grid")
        self.output_texto(texto)

    def analizar_semantico(self):
        # Primero realizar análisis sintáctico para construir el AST
        self.compilador.analizador_sintactico.analizar(self.obtener_input())

        # Si hay errores sintácticos, mostrarlos y no continuar con el análisis semántico
        if self.compilador.analizador_sintactico.errores:
            texto = "ERRORES SINTACTICOS \n"
            texto += "-" * 20 + "\n"
            texto += "Se encontraron errores sintácticos. Corríjalos antes de realizar el análisis semántico.\n"
            texto += tabulate(self.compilador.analizador_sintactico.errores, headers="keys", tablefmt="grid")
            self.output_texto(texto)
            return

        # Realizar análisis semántico
        self.compilador.analizar(self.obtener_input())

        # Mostrar resultados
        texto = "ANALISIS SEMANTICO \n"
        texto += "-" * 20 + "\n"

        # Mostrar variables declaradas
        texto += "Variables declaradas:\n"
        variables_info = []
        for var, tipo in self.compilador.variables_declaradas.items():
            variables_info.append({"Variable": var, "Tipo": tipo})
        texto += tabulate(variables_info, headers="keys", tablefmt="grid")
        texto += "\n"

        # Mostrar errores semánticos
        texto += "Errores semánticos encontrados:\n"
        if self.compilador.errores:
            texto += tabulate(self.compilador.errores, headers="keys", tablefmt="grid")
        else:
            texto += "No se encontraron errores semánticos.\n"

        self.output_texto(texto)

if __name__ == "__main__":
    app = Ventana()
    app.ventana.mainloop()
