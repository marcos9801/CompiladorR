# Importar las clases necesarias
from analizador_lexico.analizador_lexico import AnalizadorLexicoR # Asumiendo que tenemos el lexer
from analizador_sintactico.analizador_sintactico import AnalizadorSintacticoR

# Crear instancia del lexer
lexer = AnalizadorLexicoR()

# Crear instancia del parser
parser = AnalizadorSintacticoR(lexer.tokens)

# Ejemplo de código R para analizar
codigo_r = """
suma <- function(a, b) {
    return(a + b)
}

resultado <- suma(5, 3)
x <- 10 * (5 + 3)
"""

# Realizar el análisis
try:
    resultado = parser(codigo_r, lexer.tokens)
    print("Análisis sintáctico exitoso!")
    print("Árbol de análisis sintáctico:", resultado)
except Exception as e:
    print("Error durante el análisis:", str(e))
