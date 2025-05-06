from analizador_semantico.analizador_semantico import AnalizadorSemanticoR

# Código de prueba con errores semánticos
codigo_r = """
# Variables declaradas correctamente
x <- 10
y <- 20
cadena <- "Hola mundo"
booleano <- TRUE

# Uso de variable no declarada
z <- w + 5

# Incompatibilidad de tipos en condición
if (cadena > x) {
    print("Error de tipos")
}

# Variable no declarada en print
print(variable_no_declarada)

# Switch con variable no declarada
resultado <- switch(operacion_no_declarada, 
    suma = x + y,
    resta = x - y,
    "operación no soportada"
)
"""

# Crear instancia del analizador semántico
analizador_semantico = AnalizadorSemanticoR()

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