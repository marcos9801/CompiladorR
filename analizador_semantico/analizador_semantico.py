from analizador_sintactico.analizador_sintactico import AnalizadorSintacticoR
class AnalizadorSemanticoR:
    def __init__(self):
        self.analizador_sintactico = AnalizadorSintacticoR()

    def inicializar_analisis(self, codigo):
        self.analizador_sintactico.analizar(codigo)