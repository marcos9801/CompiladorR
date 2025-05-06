from analizador_sintactico.analizador_sintactico import AnalizadorSintacticoR


# Código de prueba con switch que tiene coma al final
codigo_r_correcto = """
tipo_fruta <- "manzana"
color <- switch(tipo_fruta, 
    manzana = "rojo",
    platano = "amarillo",
    uva = "morado",
    "color desconocido"
)
"""

codigo_r_erroneo = """
tipo_fruta <- "manzana"
color <- switch tipo_fruta,
    manzana = "rojo",
    platano  "amarillo",
    uva = "morado",
    "color desconocido"
)
"""

# Crear instancia del analizador sintáctico
analizador_sintactico = AnalizadorSintacticoR()
seleccion = int(input("¿Desea probar el código correcto (1) o el erróneo (2)? "))

if seleccion == 1:
    codigo_r = codigo_r_correcto
elif seleccion == 2:
    codigo_r = codigo_r_erroneo
else:
    print("Selección no válida. Saliendo del programa.")
    exit()

# Analizar el código
analizador_sintactico.analizar(codigo_r)
# Imprimir el AST
print("\nÁrbol Sintáctico (AST):")

def imprimir_ast(nodo, nivel=0):
    print("  " * nivel + str(nodo.valor))
    for hijo in nodo.children:
        imprimir_ast(hijo, nivel + 1)

imprimir_ast(analizador_sintactico.AST)
print("\nErrores sintácticos:")
if analizador_sintactico.errores:
    for error in analizador_sintactico.errores:
        print(f"  - {error['mensaje']} en línea {error['linea']}, columna {error['columna']}")
else:
    print("  No se encontraron errores sintácticos.")