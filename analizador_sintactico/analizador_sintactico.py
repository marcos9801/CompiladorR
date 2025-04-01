from analizador_lexico.analizador_lexico import AnalizadorLexicoR
class AnalizadorSintacticoR:
    def __init__(self, tokens):
        #TODO: crear analizador sintactico
        #self.tokens = tokens[]
        self.variables = {}
        self.errores = []

    def analizar(self, linea):
        tokens = linea.strip().split()
        if not tokens:
            return
        if tokens[0] in AnalizadorLexicoR.patrones['TIPOS']:
            if len(tokens) >= 4 and (tokens[2] == '=' or tokens[2] == '<-' or tokens[2] == '->'):
                tipo = tokens[0]
                nombre = tokens[1]
                valor = tokens[3] #No es necesario usar strip ya que R no finaliza vcon ;
                if nombre in self.tokens:
                    self.errores.append(f"Warning: ambiguedad - variable '{nombre}' ya declarada")
                    return
                if (tipo == "numeric" or tipo == "integer") and not valor.isnumeric():
                    self.errores.append(f"Warning: tipo incorrecto - se esperaba valor numerico para '{nombre}'")
                    return
                self.variables[nombre] = {'tipo': tipo, 'valor': valor}
            else:
                self.errores.append(f"Error: declaración de variable inválida linea'{tokens}'")
        elif '=' in linea:
            self.errores.append(f"Warning: variable '{tokens[0]}' no definida")

    def analizar_codigo(self, codigo):
        lineas = codigo.split('\n')
        for linea in lineas:
            if len(linea.strip()) > 0:
                self.analizar(linea)
        return self.errores

if __name__ == '__main__':
    pass