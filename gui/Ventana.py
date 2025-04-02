from tkinter import Tk, Menu, PhotoImage, Entry, Text
from os import path
from tabulate import tabulate

from analizador_semantico.analizador_semantico import AnalizadorSemanticoR

directorio_actual = path.dirname(__file__) 

class Ventana:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Compilador lenguaje R")
        self.ventana.geometry("800x600")
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
        self.menuSuperior()
        self.compilador = AnalizadorSemanticoR()
        self.editores()

    def menu_archivo(self):

        menu_archivo = Menu(self.menu, tearoff=0)
        menu_archivo.add_command(label="Guardar", accelerator="Ctrl+G", image=self.save_icon, compound="left")
        menu_archivo.add_command(label="Limpiar pantalla", accelerator="Ctrl+L", image=self.clean_icon, compound="left")
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
        menu_compiladores.add_command(label="Analizador Semántico", accelerator="Alt+M", image=self.semantico_icon, compound="left")
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

    def editores(self):
        # Crear caja de texto principal para el código
        self.editor = Text(self.ventana, width=100, height=30)
        self.editor.pack(pady=0, padx=0)
        # Crear caja de texto para la salida/resultados
        self.output = Text(self.ventana, width=100, height=10, state='disabled')
        self.output.pack(pady=10, padx=10)
        # Configurar colores y fuentes
        self.editor.configure(bg='white', fg='black', font=('Courier', 12))
        self.output.configure(bg='lightgray', fg='black', font=('Courier', 12))

    def output_texto(self, texto):
        """
        Módulo para imprimir texto en la salida del texto
        :param texto: El texto que se mostrará en la caja de salida
        :return: None
        """
        self.output.configure(state='normal')
        self.output.insert('end', texto + '\n')
        self.output.see('end')
        self.output.configure(state='disabled')

    def obtener_input(self):
        return self.editor.get("1.0", "end-1c")
    def analizar_sintactico(self):
        self.output_texto(self.obtener_input())

    def analizar_lexico(self):
        self.compilador.analizador_sintactico.analizador_lexico.analizar(self.obtener_input())
        texto = "ANALISIS LEXICO \n"
        texto += "-" * 20 + "\n"
        print("pasa aqui")
        texto += tabulate( self.compilador.analizador_sintactico.analizador_lexico.tokens, headers="keys", tablefmt="grid")
        texto += "\n"
        texto += "Errores Encontrados"
        texto += tabulate( self.compilador.analizador_sintactico.analizador_lexico.errores, headers="keys", tablefmt="grid")
        self.output_texto(texto)
        pass

if __name__ == "__main__":
    app = Ventana()
    app.ventana.mainloop()
