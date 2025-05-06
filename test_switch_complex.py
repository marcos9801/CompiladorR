from analizador_sintactico.analizador_sintactico import AnalizadorSintacticoR

# Código de prueba con switch que tiene expresiones más complejas
codigo_r = """
x <- 2
T <- TRUE

# Switch con expresiones complejas como valores
resultado <- switch(operacion, 
    suma = (x + 5),
    resta = (x - 3),
    multiplicacion = (x * 2),
    division = (x / 1),
    "operacion no soportada"
)

"""

# Crear instancia del analizador sintáctico
analizador_sintactico = AnalizadorSintacticoR()

# Analizar el código
analizador_sintactico.analizar(codigo_r)

# Verificar si hay errores sintácticos
print("\nErrores sintácticos:")
if analizador_sintactico.errores:
    for error in analizador_sintactico.errores:
        print(f"  - {error['mensaje']} en línea {error['linea']}, columna {error['columna']}")
else:
    print("  No se encontraron errores sintácticos.")

# Imprimir el AST
print("\nÁrbol Sintáctico (AST):")

def imprimir_ast(nodo, nivel=0):
    print("  " * nivel + str(nodo.valor))
    for hijo in nodo.children:
        imprimir_ast(hijo, nivel + 1)

imprimir_ast(analizador_sintactico.AST)