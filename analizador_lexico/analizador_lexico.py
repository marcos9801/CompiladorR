import re


class AnalizadorLexicoR:
    """
    Analizador léxico para el lenguaje R.
    Realiza el análisis token por token del código fuente y mantiene registro
    de la posición de cada token.
    """

    def __init__(self):
        """
        :param codigo:
        """
        self.codigo_fuente = ""
        self.tokens = []  # Lista para almacenar todos los tokens
        self.linea = 1  # Contador de líneas
        self.columna = 1  # Contador de columnas
        self.patrones = {
            'PALABRA_RESERVADA': r'\b(if|else|while|for|function|return|break|next|switch|TRUE|FALSE|NULL|NA|Inf|NaN|in|repeat)\b',
            'OPERADOR': r'(<-|<<-|->|=|\+|-|\*|/|%|^|&|\||!|>=|<=|==|!=|<|>)',
            'NUMERO': r'\b\d*\.\d+|\d+\b',
            'IDENTIFICADOR': r'[a-zA-Z0-9_][a-zA-Z0-9_]*',
            'CADENA_CORRECTA': r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'',
            'CADENA_INCORRECTA': r'"(?:[^"\\\n]|\\.)*(?=\n|$)|\'(?:[^\'\\\n]|\\.)*(?=\n|$)',
            'ESPACIO': r'\s+|\t',
            'COMENTARIO': r'#.*',
            'DELIMITADOR': r'[\(\)\{\}\[\],;]',
        }
        self.errores = []
        self.error = 0

    def agregar_error(self, mensaje, linea, columna, valor):
        """
        Agrega un error a la lista de errores.
        """
        self.error = 1
        error = {
            'mensaje': mensaje,
            'linea': linea,
            'columna': columna,
            'valor': valor
        }
        self.errores.append(error)

    def analizar(self, codigo):
        """
        Analiza el código fuente y genera una lista de tokens.
        """

        self.codigo_fuente = "\n" + codigo
        posicion = 0
        while posicion < len(self.codigo_fuente):
            match = None
            char = self.codigo_fuente[posicion]
            # Manejo de nueva línea
            if char == '\n':
                token = {
                    'tipo': 'SALTO_LINEA',
                    'valor': char,
                    'linea': self.linea,
                    'columna': self.columna
                }
                self.tokens.append(token)
                self.linea += 1
                self.columna = 1
                posicion += 1
                continue

            for tipo_token, patron in self.patrones.items():
                regex = re.compile(patron)
                match = regex.match(self.codigo_fuente, posicion)
                if match:
                    valor = match.group(0)

                    # Manejo de errores en identificadores
                    if tipo_token == 'IDENTIFICADOR' and valor[0].isdigit():
                        tipo_token+="_INVALIDO"
                        self.agregar_error(
                            "Error: Las variables no pueden iniciar con un número.",
                            self.linea, self.columna, valor
                        )

                    # Manejo de cadenas mal formadas
                    elif tipo_token == 'CADENA_INCORRECTA':
                        self.agregar_error(
                            "Error: Cadena sin cerrar.",
                            self.linea, self.columna, valor
                        )

                    # Guardar token si es válido
                    if tipo_token not in ('ESPACIO', 'COMENTARIO'):
                        token = {
                            'tipo': tipo_token,
                            'valor': valor,
                            'linea': self.linea,
                            'columna': self.columna
                        }
                        self.tokens.append(token)

                    # Actualizar posición y columna
                    nueva_posicion = match.end()
                    self.columna += nueva_posicion - posicion
                    posicion = nueva_posicion
                    break

            # Si no hay match, es un error léxico
            if not match:
                if not char.isspace():
                    self.agregar_error(
                        f"Error: Carácter no reconocido '{char}'.",
                        self.linea, self.columna, char
                    )
                posicion += 1
                self.columna += 1

        return self.tokens

    def if_analisis(self, linea):
        pass

if __name__ == '__main__':
    codigo_r = """
    1x <- 10
    c <- TRUE
    cadena -> "si
    if (x > 5) {
        print("Mayor que 5")
    }
    """
    analizador = AnalizadorLexicoR()
    tokens = analizador.analizar(codigo_r)
    print("Tokens encontrados:")
    for token in tokens:
        print(f"Tipo: {token['tipo']}, Valor: {token['valor']}, "
              f"Línea: {token['linea']}, Columna: {token['columna']}")
    print("\nErrores encontrados:")
    for error in analizador.errores:
        print(f"{error['mensaje']} (Valor: '{error['valor']}', Línea: {error['linea']}, Columna: {error['columna']})")
