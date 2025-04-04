from analizador_lexico.analizador_lexico import AnalizadorLexicoR
from analizador_sintactico.analizador_sintactico import AnalizadorSintacticoR


class AnalizadorSemanticoR:
    def __init__(self):
        self.errores = []

    def agregar_error_semantico(self, mensaje, nodo):
        self.errores.append({
            'mensaje': mensaje,
            'nodo': nodo.valor
        })

    def analizar(self, ast):
        self.errores = []
        self.verificar_nodo(ast)

    def verificar_nodo(self, nodo):
        if nodo.valor == "Programa":
            for hijo in nodo.children:
                self.verificar_nodo(hijo)
        elif nodo.valor == "sentencia":
            self.verificar_sentencia(nodo)
        elif nodo.valor == "if":
            self.verificar_if(nodo)
        elif nodo.valor == "print":
            self.verificar_print(nodo)
        elif nodo.valor == "switch":
            self.verificar_switch(nodo)
        else:
            for hijo in nodo.children:
                self.verificar_nodo(hijo)

    def verificar_sentencia(self, nodo):
        if len(nodo.children) < 3:
            self.agregar_error_semantico("Sentencia incompleta", nodo)
        # Additional semantic checks for assignments can be added here

    def verificar_if(self, nodo):
        if len(nodo.children) < 2:
            self.agregar_error_semantico("Condición if incompleta", nodo)
        # Additional semantic checks for if conditions can be added here

    def verificar_print(self, nodo):
        if len(nodo.children) != 1:
            self.agregar_error_semantico("Sentencia print incorrecta", nodo)
        # Additional semantic checks for print statements can be added here

    def verificar_switch(self, nodo):
        if len(nodo.children) < 4:
            self.agregar_error_semantico("Sentencia switch incompleta", nodo)
        # Additional semantic checks for switch statements can be added here

if __name__ == '__main__':
    codigo_r = """
    x <- 2
    T <- TRUE
    cadena -> "si"
    color <- switch(tipo_fruta,
               manzana = "rojo",
               platano = "amarillo",
               uva = "morado",
               "color desconocido")
    if (x > 5) {
        print("Mayor que 5")
    }
    x <- 3
    """

    analizador_lexico = AnalizadorLexicoR()
    analizador_lexico.analizar(codigo_r)

    analizador_sintactico = AnalizadorSintacticoR()
    analizador_sintactico.analizar(codigo_r)

    analizador_semantico = AnalizadorSemanticoR()
    analizador_semantico.analizar(analizador_sintactico.AST)
    print("\nErrores sintacticos:")
    for error in analizador_sintactico.errores:
        print(error)
    print("\nErrores semánticos:")
    for error in analizador_semantico.errores:
        print(error)