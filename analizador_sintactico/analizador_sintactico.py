from analizador_lexico.analizador_lexico import AnalizadorLexicoR

class Nodo:
    """
    Clase que representa un nodo en el Árbol de Sintaxis Abstracta (AST).
    Cada nodo puede tener un valor y múltiples hijos.
    """
    def __init__(self, valor=None):
        """
        Inicializa un nodo con un valor opcional.

        Args:
            valor: El valor del nodo (puede ser un token, un tipo de nodo, etc.)
        """
        self.valor = valor
        self.children = []  # Lista de nodos hijos


"""    Definicion de tipos de nodos
Definicion de bloques para la sentencia 
    0 - scope global
    1 - scope if
    2 - scope switch

"""

class AnalizadorSintacticoR:
    """
    Analizador sintáctico para el lenguaje R.
    Construye un Árbol de Sintaxis Abstracta (AST) a partir de los tokens
    generados por el analizador léxico.
    """
    def __init__(self):
        """
        Inicializa el analizador sintáctico.
        """
        self.tokens = []  # Lista de tokens a analizar
        self.analizador_lexico = AnalizadorLexicoR()  # Instancia del analizador léxico
        self.posicion = 0  # Posición actual en la lista de tokens
        self.errores = []  # Lista para almacenar errores sintácticos
        self.AST = Nodo("Programa")  # Raíz del árbol de sintaxis abstracta

    def agregar_error_sintactico(self, mensaje):
        """
        Agrega un error sintáctico a la lista de errores.

        Args:
            mensaje: Descripción del error encontrado
        """
        token_actual = "fin del archivo" if self.posicion >= len(self.tokens) else f"'{self.tokens[self.posicion]['valor']}'"

        self.errores.append({
            'mensaje': f"{mensaje} (encontrado: {token_actual})",
            'linea': self.tokens[self.posicion]['linea'] if self.posicion < len(self.tokens) else "EOF",
            'columna': self.tokens[self.posicion]['columna'] if self.posicion < len(self.tokens) else "EOF",
            'valor': self.tokens[self.posicion]['valor'] if self.posicion < len(self.tokens) else "EOF"
        })

    def analizar(self, codigo_r):
        """
        Analiza el código fuente y construye el AST.

        Args:
            codigo_r: Código fuente en lenguaje R a analizar

        Returns:
            True si el análisis fue exitoso, False si hubo errores
        """
        # Realizar análisis léxico
        self.analizador_lexico.analizar(codigo_r)

        # Verificar si hubo errores léxicos
        if self.analizador_lexico.errores:
            print("Error en análisis léxico. Corrige los errores léxicos antes de continuar.")
            for error in self.analizador_lexico.errores:
                print(f"  - {error['mensaje']} en línea {error['linea']}, columna {error['columna']}")
            return False

        # Inicializar para análisis sintáctico
        self.tokens = self.analizador_lexico.tokens
        self.posicion = 0
        self.AST = Nodo("Programa")
        self.errores = []

        # Comenzar análisis sintáctico
        self.programa()

        # Verificar si hubo errores sintácticos
        return len(self.errores) == 0

    def programa(self):
        """
        Analiza el programa completo, procesando todas las declaraciones.
        Un programa es una secuencia de declaraciones.
        """
        while self.posicion < len(self.tokens):
            # Ignorar saltos de línea al inicio
            if self.posicion < len(self.tokens) and self.tokens[self.posicion]['tipo'] == "SALTO_LINEA":
                self.posicion += 1
                continue

            # Procesar la declaración
            self.declaracion(self.AST)

            # Si hubo un error en esta declaración, intentar recuperarse
            # avanzando hasta el siguiente token significativo
            if len(self.errores) > 0 and self.errores[-1]['linea'] == self.tokens[self.posicion-1]['linea'] if self.posicion > 0 else False:
                self.recuperar_de_error()

    def recuperar_de_error(self):
        """
        Intenta recuperarse de un error sintáctico avanzando hasta el siguiente
        token significativo (generalmente el inicio de la siguiente declaración).
        """
        linea_actual = self.tokens[self.posicion]['linea'] if self.posicion < len(self.tokens) else -1

        # Avanzar hasta encontrar un salto de línea o el final del archivo
        while (self.posicion < len(self.tokens) and 
               self.tokens[self.posicion]['linea'] == linea_actual):
            self.posicion += 1

    def declaracion(self, nodo, b_if=0):
        """
        Analiza una declaración y la agrega al nodo padre.
        Una declaración puede ser una sentencia if, print, o una asignación.

        Args:
            nodo: Nodo padre al que se agregará la declaración
            b_if: Indica si estamos dentro de un bloque if (para validaciones específicas)
        """
        # Verificar fin de archivo
        if self.posicion >= len(self.tokens):
            return

        # Ignorar saltos de línea
        if self.tokens[self.posicion]['tipo'] == "SALTO_LINEA":
            self.posicion += 1
            return

        token = self.tokens[self.posicion]

        # Procesar según el tipo de token
        if token['tipo'] == "PALABRA_RESERVADA":
            if token['valor'] == 'if':
                self.declaracion_if(nodo)
            elif token['valor'] == 'print':
                self.declaracion_print(nodo)
            else:
                # Palabra reservada no esperada
                self.agregar_error_sintactico(f"Palabra reservada '{token['valor']}' no esperada en este contexto")
                self.posicion += 1
        elif token['tipo'] == "IDENTIFICADOR":
            self.declaracion_sentencia(nodo, b_if)
        else:
            # Token no esperado, reportar error y avanzar
            self.agregar_error_sintactico(f"Token no esperado de tipo {token['tipo']}")
            self.posicion += 1

    def declaracion_print(self, nodo):
        """
        Analiza una sentencia print y la agrega al nodo padre.
        Formato esperado: print(<expresión>)

        Args:
            nodo: Nodo padre al que se agregará la sentencia print
        """
        # Verificar que hay suficientes tokens para formar una sentencia print válida
        if self.posicion >= len(self.tokens) - 3:
            self.agregar_error_sintactico("Sentencia print incompleta")
            return

        # Crear nodo para la sentencia print
        n_print = Nodo("print")

        # Avanzar después de 'print'
        self.posicion += 1

        # Verificar paréntesis de apertura
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != '(':
            self.agregar_error_sintactico("Se esperaba un paréntesis de apertura '(' después de print")
            return

        # Agregar paréntesis de apertura al AST
        n_print.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1

        # Verificar que hay un token para imprimir
        if self.posicion >= len(self.tokens):
            self.agregar_error_sintactico("Se esperaba una expresión dentro del print")
            return

        # Crear nodo para el contenido a imprimir
        contenido = Nodo("contenido")

        # Verificar el tipo de contenido
        if self.tokens[self.posicion]['tipo'] in ["CADENA_CORRECTA", "NUMERO", "IDENTIFICADOR"]:
            contenido.children.append(Nodo(self.tokens[self.posicion]['valor']))
        else:
            self.agregar_error_sintactico("Tipo de expresión no válido para print")
            return

        # Agregar contenido al nodo print
        n_print.children.append(contenido)
        self.posicion += 1

        # Verificar paréntesis de cierre
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != ')':
            self.agregar_error_sintactico("Se esperaba un paréntesis de cierre ')' para cerrar el print")
            return

        # Agregar paréntesis de cierre al AST
        n_print.children.append(Nodo(self.tokens[self.posicion]['valor']))
        self.posicion += 1

        # Agregar la sentencia print completa al nodo padre
        nodo.children.append(n_print)

    def declaracion_if(self, nodo):
        """
        Analiza una sentencia if y la agrega al nodo padre.
        Formato esperado: if (<condición>) { <bloque> }

        Args:
            nodo: Nodo padre al que se agregará la sentencia if
        """
        # Crear nodo para la sentencia if
        nodo_if = Nodo("if")

        # Avanzar después de 'if'
        self.posicion += 1

        # Verificar si la condición está entre paréntesis (opcional en R)
        tiene_parentesis = False
        if self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] == "(":
            tiene_parentesis = True
            nodo_if.children.append(Nodo(self.tokens[self.posicion]['valor']))  # Agregar '(' al AST
            self.posicion += 1

        # Crear nodo para la condición
        condicion = Nodo("Condición")

        # Procesar la condición
        # En R, la condición puede ser una expresión compleja
        # Aquí procesamos una condición simple: <identificador> <operador> <valor>

        # Verificar que hay suficientes tokens para la condición
        if self.posicion >= len(self.tokens):
            self.agregar_error_sintactico("Condición del if incompleta")
            return

        # Primer elemento de la condición (generalmente un identificador)
        if self.tokens[self.posicion]['tipo'] in ["IDENTIFICADOR", "NUMERO"]:
            condicion.children.append(Nodo(self.tokens[self.posicion]['valor']))
            self.posicion += 1
        else:
            self.agregar_error_sintactico("Se esperaba un identificador o número en la condición")
        # Operador de comparación
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] not in [">", "<", "==", ">=", "<="]:
            self.agregar_error_sintactico("Se esperaba un operador de comparación (>, <, ==, >=, <=)")
        else:
            condicion.children.append(Nodo(self.tokens[self.posicion]['valor']))
            self.posicion += 1

        # Segundo elemento de la condición
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['tipo'] not in ["IDENTIFICADOR", "NUMERO", "PALABRA_RESERVADA"]:
            self.agregar_error_sintactico("Se esperaba un identificador, número o valor booleano en la condición")
        else:
            condicion.children.append(Nodo(self.tokens[self.posicion]['valor']))
            self.posicion += 1

        # Si la condición tenía paréntesis, verificar el cierre

        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] == ")":
            if not tiene_parentesis:
                self.agregar_error_sintactico("Se esperaba '(' para la  paertura de la condición")

        nodo_if.children.append(Nodo(self.tokens[self.posicion]['valor']))  # Agregar ')' al AST
        self.posicion += 1


        # Agregar la condición al nodo if
        nodo_if.children.append(condicion)

        # Verificar la apertura del bloque
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "{":
            self.agregar_error_sintactico("Se esperaba '{' para el bloque del if")
        else:
            nodo_if.children.append(Nodo(self.tokens[self.posicion]['valor']))  # Agregar '{' al AST
            self.posicion += 1

        # Crear nodo para el bloque de código
        bloque = Nodo("Cuerpo_if")

        # Procesar las declaraciones dentro del bloque
        while self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != "}":
            self.declaracion(bloque, True)

        # Verificar el cierre del bloque
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "}":
            self.agregar_error_sintactico("Se esperaba '}' para cerrar el bloque del if")
            return
        nodo_if.children.append(Nodo(self.tokens[self.posicion]['valor']))  # Agregar '}' al AST
        self.posicion += 1

        # Agregar el bloque al nodo if
        nodo_if.children.append(bloque)

        # Agregar la sentencia if completa al nodo padre
        nodo.children.append(nodo_if)

    def eliminar_saltos_linea(self):
        while self.posicion < len(self.tokens) and self.tokens[self.posicion]['tipo'] == "SALTO_LINEA":
            self.posicion += 1
    def declaracion_sentencia(self, nodo, b_if=0):
        """
        Analiza una sentencia (asignación o comparación) y la agrega al nodo padre.
        Formatos esperados: 
          - Asignación: <identificador> <operador_asignacion> <valor>
          - Comparación: <identificador> <operador_comparacion> <valor>

        Args:
            nodo: Nodo padre al que se agregará la sentencia
            b_if: Indica si estamos dentro de un bloque if (para validaciones específicas)
        """
        # Verificar que hay suficientes tokens para formar una sentencia válida
        if self.posicion >= len(self.tokens) - 1:  # Necesitamos al menos identificador y operador
            self.agregar_error_sintactico("Sentencia incompleta")
            self.posicion += 1
            return

        # Crear nodo para la sentencia
        nodo_sentencia = Nodo("sentencia")

        # Verificar el identificador
        if self.tokens[self.posicion]['tipo'] != "IDENTIFICADOR":
            self.agregar_error_sintactico("Se esperaba un identificador al inicio de la sentencia")
            return

        # Agregar identificador al AST
        identificador = Nodo("identificador")
        identificador.children.append(Nodo(self.tokens[self.posicion]['valor']))
        nodo_sentencia.children.append(identificador)
        self.posicion += 1

        # Verificar el operador según el contexto
        if self.posicion >= len(self.tokens):
            self.agregar_error_sintactico("Sentencia incompleta, falta operador")
            return

        # Determinar el tipo de operador esperado según el contexto
        if b_if !=  1:  # Estamos en una asignación global o dentro de un switch
            operadores_validos = ["<-", "->", "="]
            tipo_operador = "asignación"
        else:  # Estamos en una comparación (dentro de un if)
            operadores_validos = ["<", ">", "==", ">=", "<=", "!="]
            tipo_operador = "comparación"

        # Verificar que el operador es válido para el contexto
        if self.tokens[self.posicion]['valor'] not in operadores_validos:
            self.agregar_error_sintactico(f"Se esperaba un operador de {tipo_operador} ({', '.join(operadores_validos)})")
            return

        # Agregar operador al AST
        operador = Nodo("operador")
        operador.children.append(Nodo(self.tokens[self.posicion]['valor']))
        nodo_sentencia.children.append(operador)
        self.posicion += 1

        # Verificar si el valor asignado es un switch
        if self.tokens[self.posicion]['tipo'] == "PALABRA_RESERVADA" and self.tokens[self.posicion]['valor'] == "switch":
            self.declaracion_switch(nodo_sentencia)
            nodo.children.append(nodo_sentencia)
            return

        # Verificar que hay un valor para asignar
        if self.posicion >= len(self.tokens):
            self.agregar_error_sintactico(f"Sentencia incompleta, falta valor después del operador de {tipo_operador}")
            nodo.children.append(nodo_sentencia)  # Agregar la sentencia incompleta al AST para análisis semántico
            return

        # Verificar que el valor es de un tipo válido
        tipos_validos = ["PALABRA_RESERVADA", "NUMERO", "CADENA_CORRECTA", "IDENTIFICADOR"]
        if self.tokens[self.posicion]['tipo'] not in tipos_validos:
            self.agregar_error_sintactico(f"Valor asignado inválido. Se esperaba un número, cadena, identificador o palabra reservada")
            return

        # Agregar valor al AST
        valor = Nodo("valor")
        valor.children.append(Nodo(self.tokens[self.posicion]['valor']))
        nodo_sentencia.children.append(valor)
        self.posicion += 1

        # Validar que la sentencia termina correctamente
        if b_if == 0:
            if self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != "\n":
                self.agregar_error_sintactico("Se esperaba un sañtpo de linea al final de la sentencia")
                return
        elif b_if == 1:
            if self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != "}":
                self.agregar_error_sintactico("Se esperaba '}' para cerrar el bloque del if")
                return
        elif b_if == 2:
            if  self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != (','):
                self.agregar_error_sintactico("Se esperaba ',' después del valor en la sentencia del switch")
                return

        self.posicion += 1
        # Agregar la sentencia completa al nodo padre
        nodo.children.append(nodo_sentencia)

    def procesar_valor_default(self, token, nodo_switch):
        """
        Procesa un valor por defecto en un switch y lo agrega al nodo switch.

        Args:
            token: Token que contiene el valor por defecto
            nodo_switch: Nodo al que se agregará el valor por defecto
        """
        # Crear nodo para el valor por defecto
        nodo_default = Nodo("default")

        # Verificar si es un tipo básico
        if token['tipo'] in ["CADENA_CORRECTA", "NUMERO", "IDENTIFICADOR", "PALABRA_RESERVADA"]:
            nodo_default.children.append(Nodo(token['valor']))
            nodo_switch.children.append(nodo_default)
            return True
        # Para expresiones más complejas, se podría implementar un procesamiento similar al de los valores de caso
        # Por ahora, solo aceptamos tipos básicos para el valor por defecto
        else:
            self.agregar_error_sintactico("Valor por defecto inválido en el switch. Debe ser una cadena, número, identificador o palabra reservada.")
            return False

    def declaracion_switch(self, nodo_sentencia):
        """
        Analiza una sentencia switch y la agrega al nodo padre.
        Formato esperado: switch(variable, case1 = valor1, case2 = valor2, ..., default_value)

        Args:
            nodo_sentencia: Nodo padre al que se agregará la sentencia switch
        """
        # Crear nodo para la sentencia switch
        nodo_switch = Nodo("switch")

        # Avanzar después de 'switch'
        self.posicion += 1

        # Verificar paréntesis de apertura
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != "(":
            self.agregar_error_sintactico("Se esperaba '(' después de switch")

        # Agregar paréntesis de apertura al AST
        self.posicion += 1

        # Verificar variable a evaluar
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['tipo'] != "IDENTIFICADOR":
            self.agregar_error_sintactico("Se esperaba un identificador para la variable a evaluar en el switch")

        # Agregar variable al AST
        variable = Nodo("variable")
        variable.children.append(Nodo(self.tokens[self.posicion]['valor']))
        nodo_switch.children.append(variable)
        self.posicion += 1

        # Verificar coma después de la variable
        if self.posicion >= len(self.tokens) or self.tokens[self.posicion]['valor'] != ",":
            self.agregar_error_sintactico("Se esperaba ',' después del identificador en el switch")

        # Avanzar después de la coma
        self.posicion += 1

        # Procesar casos y valor por defecto
        casos_procesados = 0

        while self.posicion < len(self.tokens) and self.tokens[self.posicion]['valor'] != ")":
            # Ignorar saltos de línea
            self.eliminar_saltos_linea()
            # Verificar si es el valor por defecto (último valor antes del paréntesis de cierre)
            # En R, el valor por defecto puede ser una cadena, número, identificador o palabra reservada
            if self.posicion + 1 < len(self.tokens) and self.tokens[self.posicion + 1]['tipo'] != "OPERADOR":
                # Procesar el valor por defecto
                valor_defecto = self.tokens[self.posicion]
                self.posicion += 1
                self.eliminar_saltos_linea()
                if self.tokens[self.posicion]['valor'] != ")":
                    self.agregar_error_sintactico("Se esperaba un valor por defecto antes de cerrar el switch")
                    return
                self.procesar_valor_default(valor_defecto, nodo_switch)
                self.posicion += 1
                break
            nodo_case = Nodo("case")
            if self.posicion + 3 >= len(self.tokens) : # no es posible procesar la declaracion
                return
            else:
                self.declaracion_sentencia(nodo_case, 2)
            nodo_switch.children.append(nodo_case)
            casos_procesados += 1

        # Verificar que se procesó al menos un caso
        if casos_procesados == 0:
            self.agregar_error_sintactico("El switch debe tener al menos un caso")


        self.eliminar_saltos_linea()

        # Agregar el switch completo a la sentencia
        nodo_sentencia.children.append(nodo_switch)

if __name__ == '__main__':
    codigo_r = """
    x <- 2
    T <- TRUE
    cadena -> "si"

    color <- switch(tipo_fruta, 
        manzana = "rojo",
        platano = "amarillo",
        uva = "morado",
        "color desconocido"
    )

    if (x > 5) { 
        print("Mayor que 5")
    } 

    x <- 3
    y <- 2
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
