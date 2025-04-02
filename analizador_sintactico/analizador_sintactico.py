from analizador_lexico.analizador_lexico import AnalizadorLexicoR


class Nodo:
    def __init__(self, valor=None):
        self.valor = valor
        self.children = []


class AnalizadorSintacticoR:
    def __init__(self):
        self.tokens = []
        self.analizador_lexico = AnalizadorLexicoR()
        self.posicion = 0
        self.errores = []
        self.AST = Nodo("Programa")

    def agregar_error_sintactico(self, mensaje):
        self.errores.append({
            'mensaje': mensaje,
            'linea': self.tokens[self.posicion]['linea'] if self.posicion < len(self.tokens) else "EOF",
            'columna': self.tokens[self.posicion]['columna'] if self.posicion < len(self.tokens) else "EOF",
            'valor': self.tokens[self.posicion]['valor'] if self.posicion < len(self.tokens) else "EOF"
        })

    def analizar(self, codigo_r):
        self.analizador_lexico.analizar(codigo_r)
        if self.analizador_lexico.errores:
            print("Error en análisis léxico")
            return

        self.tokens = self.analizador_lexico.tokens
        self.posicion = 0
        self.AST = Nodo("Programa")
        self.errores = []

        self.programa()

    def programa(self):
        while self.posicion < len(self.tokens):
            self.declaracion()

    def declaracion(self):
        if self.posicion >= len(self.tokens):
            return
        token = self.tokens[self.posicion]
        if token['tipo'] == "PALABRA_RESERVADA":
            if token['valor'] == 'if':
                self.declaracion_if()
        elif token['tipo'] == "IDENTIFICADOR":
            self.declaracion_sentencia()
        else:
            self.posicion += 1

    def declaracion_if(self):
        nodo_if = Nodo("if")
        self.posicion += 1  # Avanzar para procesar la condición

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "(":
            self.agregar_error_sintactico("Se esperaba '(' después de if")
            return

        self.posicion += 1  # Avanzar después del '('
        condicion = Nodo("Condición")

        while self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != ")":
            condicion.children.append(Nodo(self.tokens[self.posicion]['valor']))
            self.posicion += 1

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != ")":
            self.agregar_error_sintactico("Se esperaba ')' para cerrar la condición")
            return

        self.posicion += 1  # Avanzar después del ')'
        nodo_if.children.append(condicion)

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "{":
            self.agregar_error_sintactico("Se esperaba '{' para el bloque del if")
            return

        self.posicion += 1  # Avanzar después del '{'
        bloque = Nodo("Cuerpo_if")

        while self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != "}":
            self.declaracion()
            bloque.children.append(self.AST.children[-1])
            self.AST.children.pop()

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "}":
            self.agregar_error_sintactico("Se esperaba '}' para cerrar el bloque del if")
            return

        self.posicion += 1  # Avanzar después del '}'
        nodo_if.children.append(bloque)
        self.AST.children.append(nodo_if)

    def declaracion_sentencia(self):
        if self.posicion >= len(self.tokens) - 2:  # Evita acceso fuera de rango
            self.agregar_error_sintactico("Sentencia incorrecta")
            return

        nodo_sentencia = Nodo("sentencia")

        # Identificador
        if self.tokens[self.posicion]['tipo'] != "IDENTIFICADOR":
            self.agregar_error_sintactico("Se esperaba un identificador")
            return
        nodo_sentencia.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1

        # Operador de asignación
        if self.tokens[self.posicion]['valor'] not in ("<-", "->", "="):
            self.agregar_error_sintactico("Se esperaba un operador de asignación (<-, ->, =)")
            return
        nodo_sentencia.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1

        # Valor asignado
        if self.tokens[self.posicion]['tipo'] not in ("PALABRA_RESERVADA", "NUMERO", "CADENA_CORRECTA"):
            self.agregar_error_sintactico("Valor asignado inválido")
            return
        nodo_sentencia.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1

        # Validar que termina en una nueva línea
        if self.posicion < len(self.tokens) and self.tokens[self.posicion]['tipo'] != "SALTO_LINEA":
            self.agregar_error_sintactico("Sentencia debe terminar en una nueva línea")

        # Agregar al AST
        self.AST.children.append(nodo_sentencia)


if __name__ == '__main__':
    codigo_r = """
    x <- 2 T <- TRUE
    cadena -> "si"

    if (x > 5) {
        print("Mayor que 5")
    }
    x <- 3
    """

    analizador_lexico = AnalizadorLexicoR()
    analizador_lexico.analizar(codigo_r)

    print("Tokens generados:")
    for token in analizador_lexico.tokens:
        print(token)

    analizador_sintactico = AnalizadorSintacticoR()
    analizador_sintactico.analizar(codigo_r)

    print("\nErrores sintácticos:")
    for error in analizador_sintactico.errores:
        print(error)

    print("\nÁrbol Sintáctico (AST):")


    def imprimir_ast(nodo, nivel=0):
        print("  " * nivel + str(nodo.valor))
        for hijo in nodo.children:
            imprimir_ast(hijo, nivel + 1)


    imprimir_ast(analizador_sintactico.AST)
