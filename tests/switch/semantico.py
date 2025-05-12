from analizador_semantico.analizador_semantico import AnalizadorSemanticoR


# Código de prueba con switch que tiene coma al final
codigo_r_correcto = """
tipo_fruta <- "manzana"
color <- switch("", 
    manzana = "rojo",
    platano = "amarillo",
    uva = "morado",
    "color desconocido"
)
"""

codigo_r_erroneo = """
#TODO: generear archico de error semantico 
tipo_fruta <- "manzana"
color <- switch tipo_fruta,
    manzana = "rojo",
    platano  "amarillo",
    uva = "morado",
    "color desconocido"
)
"""

# Crear instancia del analizador sintáctico
analizador_semantico = AnalizadorSemanticoR()
seleccion = int(input("¿Desea probar el código correcto (1) o el erróneo (2)? "))

if seleccion == 1:
    codigo_r = codigo_r_correcto
elif seleccion == 2:
    codigo_r = codigo_r_erroneo
else:
    print("Selección no válida. Saliendo del programa.")
    exit()

# Analizar el código
analizador_semantico.analizar(codigo_r)
# Mostrar variables declaradas
print("\nVariables declaradas:")
for var, tipo in analizador_semantico.variables_declaradas.items():
    print(f"  - {var}: {tipo}")

# Verificar si hay errores semánticos
print("\nErrores semánticos:")
if analizador_semantico.errores:
    for error in analizador_semantico.errores:
        linea_info = f" en línea {error['linea']}" if error['linea'] != "desconocida" else ""
        print(f"  - {error['mensaje']}{linea_info}")
else:
    print("  No se encontraron errores semánticos.")