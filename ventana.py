from tkinter import Tk, Menu
from os import path

directorio_actual = path.dirname(__file__) 

class Ventana:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Compilador")
        self.ventana.geometry("800x600")
        self.menuSuperior()
        self.ventana.mainloop()

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
        menu_archivo = Menu(self.menu, tearoff=0)
        #menu_archivo.add_command(label="Abrir", image=PhotoImage(file=directorio_actual + "/Icons/abrir.png"))
        menu_archivo.add_command(label="Guardar", accelerator="Ctrl+G")
        menu_archivo.add_command(label="Limpiar pantalla", accelerator="Ctrl+L")
        menu_archivo.add_command(label="Cerrar", accelerator="Ctrl+W")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.quit, accelerator="Ctrl+Q")
        # Menú Editar   
        menu_editar = Menu(self.menu, tearoff=0)
        #menu Ejecutar
        menu_ejecutar =Menu(self.menu, tearoff=0)
        #menu Compiladores
        menu_compiladores = Menu(self.menu, tearoff=0)
        menu_compiladores.add_command(label="Analisador Léxico", accelerator="Alt+L")
        menu_compiladores.add_command(label="Analisador Sintáctico", accelerator="Alt+S")
        menu_compiladores.add_command(label="Analisador Semántico", accelerator="Alt+M")
        menu_compiladores.add_command(label="Generador de Código")
        menu_compiladores.add_command(label="Codigo Objeto")
        # Menú Ayuda
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
        #depois
        #meu variables
        menu_variables = Menu(self.menu, tearoff=0)
        menu_tipos = Menu(menu_variables, tearoff=0)
        menu_variables.add_cascade(label="Tipos", menu=menu_tipos)
        menu_tipos.add_command(label="int")
        menu_tipos.add_command(label="float")
        menu_tipos.add_command(label="char")
        menu_tipos.add_command(label="double")

        # Agregar al menú principal
        self.menu.add_cascade(label="Archivo", menu=menu_archivo)
        self.menu.add_cascade(label="Editar", menu=menu_editar)
        self.menu.add_cascade(label="Ejecutar", menu=menu_ejecutar)
        self.menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        self.menu.add_cascade(label="Compiladores", menu=menu_compiladores)
        self.menu.add_cascade(label="Variables", menu=menu_variables)

        self.ventana.config(menu=self.menu)

if __name__ == "__main__":
    Ventana()
