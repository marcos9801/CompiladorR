import re  # Importación

class AnalizadorLexicoR:
    def __init__(self):
        self.tokens = []
        # Definir patrones
        self.patrones = {
            'PALABRA_RESERVADA': r'\b(if|else|while|for|function|return|break|next|TRUE|FALSE|NULL|NA|Inf|NaN|in|repeat)\b',
            'OPERADOR': r'(<-|<<-|->|=|\+|-|\*|/|%|^|&|\||!|>=|<=|==|!=|<|>)',
            'NUMERO': r'\d+\.\d+|\d+',  # Asegurar que haya al menos un dígito
            'IDENTIFICADOR': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'CADENA': r'"[^"]*"|\'[^\']*\'',
            'ESPACIO': r'\s+',  # Maneja espacios y saltos de línea
            'COMENTARIO': r'#.*'
        }

    def analizar(self, codigo):
        posicion = 0
        #print("Iniciando analizador")
        while posicion < len(codigo):
            #print(f"Posición actual: {posicion} -> {codigo[posicion]!r}")
            match = None
            for tipo_token, patron in self.patrones.items():
                regex = re.compile(patron)
                match = regex.match(codigo, posicion)
                if match:
                    valor = match.group(0)
                    if not valor:  # Evitar coincidencias vacías
                        continue
                    #print(f"Coincidencia: {valor!r} ({tipo_token})")
                    if tipo_token not in ('ESPACIO', 'COMENTARIO'):
                        self.tokens.append((tipo_token, valor))
                    nueva_posicion = match.end()
                    if nueva_posicion > posicion:
                        posicion = nueva_posicion
                    else:
                        posicion += 1  # Evitar bucle infinito
                    break
            if not match:
                #print(f"No se encontró coincidencia para {codigo[posicion]!r}, avanzando 1 posición.")
                posicion += 1
        return self.tokens

if __name__ == '__main__':
    # Ejemplo de código R
    codigo_r = """
    x <- 10
    if (x > 5) {
        print("Mayor que 5")
    }"""
    print(codigo_r)
    analizador = AnalizadorLexicoR()
    tokens = analizador.analizar(codigo_r)
    for token in tokens:
        print(f"Tipo: {token[0]}, Valor: {token[1]}")
