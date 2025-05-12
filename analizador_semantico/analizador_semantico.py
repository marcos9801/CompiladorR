from analizador_lexico.analizador_lexico import AnalizadorLexicoR
from analizador_sintactico.analizador_sintactico import AnalizadorSintacticoR


class AnalizadorSemanticoR:
    def __init__(self):
        self.errores = []
        self.analizador_sintactico = AnalizadorSintacticoR()
        self.variables_declaradas = {}  # Diccionario para almacenar variables declaradas y sus tipos

    def agregar_error_semantico(self, mensaje, nodo):
        """
        Agrega un error semántico a la lista de errores con información detallada.

        Args:
            mensaje: Descripción del error
            nodo: Nodo del AST donde se encontró el error
        """
        # Buscar información de línea y columna en los tokens
        linea = "desconocida"
        columna = "desconocida"

        # Intentar encontrar un token que coincida con el valor del nodo
        for token in self.analizador_sintactico.tokens:
            if 'valor' in token and token['valor'] == nodo.valor:
                linea = token['linea']
                columna = token['columna']
                break

        self.errores.append({
            'mensaje': mensaje,
            'nodo': nodo.valor,
            'linea': linea,
            'columna': columna
        })

    def analizar(self, codigo_r):
        self.errores = []
        self.variables_declaradas = {}  # Reiniciar el diccionario de variables declaradas
        self.analizador_sintactico.analizar(codigo_r)
        self.verificar_nodo(self.analizador_sintactico.AST)

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
        # Aquí puedes agregar más verificaciones semánticas para otros nodo
    def verificar_sentencia(self, nodo):
        if len(nodo.children) < 3:
            self.agregar_error_semantico("Sentencia incompleta", nodo)
            return

        # Verificar si es una asignación
        if nodo.children[1].valor == "operador" and nodo.children[1].children[0].valor in ["<-", "->", "="]:
            # Obtener el nombre de la variable
            if nodo.children[0].valor == "identificador" and len(nodo.children[0].children) > 0:
                nombre_variable = nodo.children[0].children[0].valor

                # Verificar si hay un valor para asignar
                if len(nodo.children) >= 3:
                    # Verificar si el valor contiene variables no declaradas
                    if nodo.children[2].valor == "switch":
                        self.verificar_switch(nodo)
                    self.verificar_variables_en_expresion(nodo.children[2])
                    # Determinar el tipo del valor asignado
                    tipo_valor = self.determinar_tipo_valor(nodo.children[2])
                    # Registrar la variable declarada
                    self.variables_declaradas[nombre_variable] = tipo_valor
                else:
                    self.agregar_error_semantico(f"Falta valor para asignar a la variable '{nombre_variable}'", nodo)
            else:
                self.agregar_error_semantico("Identificador de variable inválido", nodo)

    def verificar_variables_en_expresion(self, nodo_valor):
        """
        Verifica que todas las variables usadas en una expresión estén declaradas.
        """
        if len(nodo_valor.children) == 0:
            return

        # Obtener el valor
        valor = nodo_valor.children[0].valor

        # Si el valor no es un número, una cadena o un booleano, verificar si es una variable declarada
        if not valor.isdigit() and not valor.startswith('"') and valor not in ["TRUE", "FALSE"]:
            # Si contiene operadores aritméticos, es una expresión
            if "+" in valor or "-" in valor or "*" in valor or "/" in valor:
                # Dividir la expresión en tokens
                import re
                tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+|\+|\-|\*|\/|\(|\)', valor)

                # Verificar cada token que podría ser una variable
                for token in tokens:
                    if token.isalpha() and token not in self.variables_declaradas:
                        self.agregar_error_semantico(f"Variable '{token}' usada en expresión pero no declarada", nodo_valor)
            # Si no es una expresión, verificar si es una variable declarada
            elif valor == 'identificador' and valor not in self.variables_declaradas:
                self.agregar_error_semantico(f"Variable '{valor}' usada pero no declarada", nodo_valor)

    def determinar_tipo_valor(self, nodo_valor):
        """
        Determina el tipo de un valor basado en su nodo en el AST.
        """
        if len(nodo_valor.children) == 0:
            return "desconocido"

        valor = nodo_valor.children[0].valor

        # Verificar si es un número
        if valor.isdigit() or (valor[0] == '-' and valor[1:].isdigit()):
            return "numerico"
        # Verificar si es una cadena
        elif valor.startswith('"') and valor.endswith('"'):
            return "cadena"
        # Verificar si es un booleano
        elif valor in ["TRUE", "FALSE"]:
            return "booleano"
        # Verificar si es una variable
        elif valor in self.variables_declaradas:
            return self.variables_declaradas[valor]
        # Si no se puede determinar, retornar desconocido
        else:
            return "desconocido"

    def verificar_if(self, nodo):
        if len(nodo.children) < 2:
            self.agregar_error_semantico("Condición if incompleta", nodo)
            return

        # Buscar el nodo de condición
        condicion_encontrada = False
        for hijo in nodo.children:
            if hijo.valor == "Condición":
                condicion_encontrada = True
                self.verificar_condicion(hijo)
                break

        if not condicion_encontrada:
            self.agregar_error_semantico("No se encontró la condición en la sentencia if", nodo)

        # Verificar el cuerpo del if
        for hijo in nodo.children:
            if hijo.valor == "Cuerpo_if":
                for sentencia in hijo.children:
                    self.verificar_nodo(sentencia)

    def verificar_condicion(self, nodo_condicion):
        """
        Verifica que las variables usadas en una condición estén declaradas
        y que los tipos sean compatibles para la operación.
        """
        if len(nodo_condicion.children) < 3:
            self.agregar_error_semantico("Condición incompleta", nodo_condicion)
            return

        # Obtener los operandos y el operador
        operando1 = nodo_condicion.children[0].valor
        operador = nodo_condicion.children[1].valor
        operando2 = nodo_condicion.children[2].valor

        if operador == 'switch':
            self.verificar_switch(nodo_condicion)
            return

        # Verificar que las variables estén declaradas
        for operando in [operando1, operando2]:
            if not operando.isdigit() and operando not in ["TRUE", "FALSE"] and not operando.startswith('"'):
                if operando not in self.variables_declaradas:
                    self.agregar_error_semantico(f"Variable '{operando}' usada en condición pero no declarada", nodo_condicion)

        # Determinar los tipos de los operandos
        tipo1 = self.determinar_tipo_operando(operando1)
        tipo2 = self.determinar_tipo_operando(operando2)

        # Verificar compatibilidad de tipos según el operador
        if operador in ["<", ">", ">=", "<="]:
            # Operadores de comparación numérica
            if tipo1 != "numerico" or tipo2 != "numerico":
                self.agregar_error_semantico(f"Operador '{operador}' requiere operandos numéricos", nodo_condicion)
        elif operador == "==":
            # Igualdad: los tipos deben ser compatibles
            if tipo1 != tipo2 and tipo1 != "desconocido" and tipo2 != "desconocido":
                self.agregar_error_semantico(f"Comparación de igualdad entre tipos incompatibles: {tipo1} y {tipo2}", nodo_condicion)

    def determinar_tipo_operando(self, operando):
        """
        Determina el tipo de un operando.
        """
        # Verificar si es un número
        if operando.isdigit() or (operando[0] == '-' and operando[1:].isdigit()):
            return "numerico"
        # Verificar si es una cadena
        elif operando.startswith('"') and operando.endswith('"'):
            return "cadena"
        # Verificar si es un booleano
        elif operando in ["TRUE", "FALSE"]:
            return "booleano"
        # Verificar si es una variable
        elif operando in self.variables_declaradas:
            return self.variables_declaradas[operando]
        # Si no se puede determinar, retornar desconocido
        else:
            return "desconocido"

    def verificar_print(self, nodo):
        if len(nodo.children) < 3:  # Debe tener al menos paréntesis de apertura, contenido y paréntesis de cierre
            self.agregar_error_semantico("Sentencia print incorrecta", nodo)
            return

        # Buscar el nodo de contenido
        for i, hijo in enumerate(nodo.children):
            if hijo.valor == "contenido" and len(hijo.children) > 0:
                contenido = hijo.children[0].valor

                # Si el contenido es un identificador (variable), verificar que esté declarado
                if not contenido.startswith('"') and not contenido.isdigit() and contenido not in ["TRUE", "FALSE"]:
                    if contenido not in self.variables_declaradas:
                        self.agregar_error_semantico(f"Variable '{contenido}' usada en print pero no declarada", nodo)

    def verificar_switch(self, nodo):
        #TODO: Refactorizar para uso de R

        if len(nodo.children) < 3:
            self.agregar_error_semantico("Sentencia switch incompleta", nodo)
            return

        # Buscar el nodo de variable (la expresión a evaluar)
        variable_encontrada = False
        for hijo in nodo.children[2].children:
            if hijo.valor == "variable" and len(hijo.children) > 0:
                variable_encontrada = True
                variable = hijo.children[0].valor

                # Verificar que la variable esté declarada
                if variable not in self.variables_declaradas:
                    self.agregar_error_semantico(f"Variable '{variable}' usada en switch pero no declarada", nodo)
                break

        if not variable_encontrada:
            self.agregar_error_semantico("No se encontró la variable a evaluar en el switch", nodo)

        # Verificar los casos del switch
        for hijo in nodo.children:
            if hijo.valor == "IDENTIFICADOR":
                self.verificar_case(hijo)
            elif hijo.valor == "default":
                # Verificar si el valor por defecto es una variable
                if len(hijo.children) > 0:
                    valor_default = hijo.children[0].valor
                    if not valor_default.isdigit() and not valor_default.startswith('"') and valor_default not in ["TRUE", "FALSE"]:
                        if valor_default not in self.variables_declaradas:
                            self.agregar_error_semantico(f"Variable '{valor_default}' usada como valor por defecto en switch pero no declarada", nodo)

    def verificar_case(self, nodo_case):
        """
        Verifica que las variables usadas en un caso de switch estén declaradas.
        """
        # Verificar el valor del caso
        for hijo in nodo_case.children:
            if hijo.valor == "IDENTIFICADOR" and len(hijo.children) > 0:
                valor = hijo.children[0].valor

                # Si el valor es un identificador (variable), verificar que esté declarado
                if not valor.startswith('"') and not valor.isdigit() and valor not in ["TRUE", "FALSE"]:
                    if valor not in self.variables_declaradas:
                        self.agregar_error_semantico(f"Variable '{valor}' usada en caso de switch pero no declarada", nodo_case)

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
