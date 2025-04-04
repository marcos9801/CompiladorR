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
            self.declaracion(self.AST)

    def declaracion(self, nodo, b_if=False):
        if self.posicion >= len(self.tokens):
            return
        token = self.tokens[self.posicion]
        if token['tipo'] == "PALABRA_RESERVADA":
            if token['valor'] == 'if':
                self.declaracion_if(nodo)
            elif token['valor'] == 'print':
                self.declaracion_print(nodo)
        elif token['tipo'] == "IDENTIFICADOR":
            self.declaracion_sentencia(nodo, b_if)
        else:
            self.posicion += 1

    def declaracion_print(self, nodo):
        if self.posicion >= len(self.tokens) - 3:
            self.agregar_error_sintactico("Sentencia print incorrecta")
            return
        n_print = Nodo("print")
        self.posicion += 1
        if self.tokens[self.posicion]['valor'] != '(':
            self.agregar_error_sintactico("Se esperaba un paréntesis de apertura")
            return
        self.posicion += 1
        n_print.children.append(Nodo(self.tokens[self.posicion]['valor']))  # agregar token a imprimir
        self.posicion += 1
        if self.tokens[self.posicion]['valor'] != ')':
            self.agregar_error_sintactico("Se esperaba un paréntesis de cierre")
            return
        self.posicion += 1
        nodo.children.append(n_print)

    def declaracion_if(self, nodo):
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
            self.declaracion(bloque, True)

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "}":
            self.agregar_error_sintactico("Se esperaba '}' para cerrar el bloque del if")
            return

        self.posicion += 1  # Avanzar después del '}'
        nodo_if.children.append(bloque)
        nodo.children.append(nodo_if)

    def declaracion_sentencia(self, nodo, b_if=False):

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
        if not b_if and self.tokens[self.posicion]['valor'] not in ("<-", "->", "="):
            self.agregar_error_sintactico("Se esperaba un operador de asignación (<-, ->, =)")
            return
        if b_if and self.tokens[self.posicion]['valor'] not in ("<", ">", "=="):
            self.agregar_error_sintactico("Se esperaba un operador de comparación (<, >, ==)")
            return
        nodo_sentencia.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1
        if self.tokens[self.posicion]['tipo'] == "PALABRA_RESERVADA" and self.tokens[self.posicion]['valor'] == "switch":
            self.declaracion_switch(nodo_sentencia)
            nodo.children.append(nodo_sentencia)
            return

        # Valor asignado
        if self.tokens[self.posicion]['tipo'] not in ("PALABRA_RESERVADA", "NUMERO", "CADENA_CORRECTA"):
            self.agregar_error_sintactico("Valor asignado inválido")
            return
        if self.tokens[self.posicion]['valor'] == "switch":
            self.declaracion_switch(nodo_sentencia)
        else:
            nodo_sentencia.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1

        # Validar que termina en una nueva línea
        if self.posicion < len(self.tokens) and self.tokens[self.posicion]['tipo'] != "SALTO_LINEA":
            self.agregar_error_sintactico("Sentencia debe terminar en una nueva línea")

        nodo.children.append(nodo_sentencia)

    def declaracion_switch(self, nodo_sentencia):
        nodo_switch = Nodo("switch")
        self.posicion += 1  # Avanzar para procesar la variable

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "(":
            self.agregar_error_sintactico("Se esperaba '(' después de switch")
            return

        nodo_switch.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1  # Avanzar después del '('

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['tipo'] != "IDENTIFICADOR":
            self.agregar_error_sintactico("Se esperaba un identificador para la variable")
            return
        nodo_switch.children.append(Nodo(self.tokens[self.posicion]['valor']))  # Agregar variable
        self.posicion += 1  # Avanzar después del identificador y la coma
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != ",":
            self.agregar_error_sintactico("Se esperaba ',' después del identificador")
            return
        self.posicion += 1  # Avanzar después de la coma

        while self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != ")":
            if self.tokens[self.posicion]['tipo'] == "SALTO_LINEA":
                self.posicion += 1
                continue
            if self.posicion < len(self.tokens) and self.tokens[self.posicion + 1]['valor'] == ")":
                nodo_default = Nodo("default")
                nodo_default.children.append(Nodo(self.tokens[self.posicion]['valor']))  # Agregar default
                nodo_switch.children.append(nodo_default)
                self.posicion += 1
                break

            if self.tokens[self.posicion]['tipo'] != "IDENTIFICADOR":
                self.agregar_error_sintactico("Se esperaba un identificador para el case")
                return
            nodo_case = Nodo("case")
            nodo_case.children.append(Nodo(self.tokens[self.posicion]['valor']))
            self.posicion += 1
            if self.tokens[self.posicion]['valor'] != "=":
                self.agregar_error_sintactico("Se esperaba '=' después del case")
                return
            nodo_case.children.append(Nodo(self.tokens[self.posicion]['valor']))
            self.posicion += 1

            if self.tokens[self.posicion]['tipo'] not in ("PALABRA_RESERVADA", "NUMERO", "CADENA_CORRECTA"):
                self.agregar_error_sintactico("Valor asignado inválido")
                return
            nodo_case.children.append(Nodo(self.tokens[self.posicion]['valor']))
            self.posicion += 1
            if self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != ",":
                self.agregar_error_sintactico("Se esperaba ',' después del case")
                return
            self.posicion += 1

            nodo_switch.children.append(nodo_case)  # Agregar case al switch

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != ")":
            self.agregar_error_sintactico("Se esperaba ')' para cerrar el switch")
            return
        nodo_switch.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1  # Avanzar después del ')'

        nodo_sentencia.children.append(nodo_switch)  # Agregar el switch a la sentencia

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