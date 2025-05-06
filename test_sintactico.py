from analizador_sintactico.analizador_sintactico import AnalizadorSintacticoR

def main():
    # Leer el archivo de prueba
    with open('prueba_sintactico', 'r') as f:
        codigo_r = f.read()
    
    print("Código a analizar:")
    print("-" * 40)
    print(codigo_r)
    print("-" * 40)
    
    # Crear instancia del analizador sintáctico
    analizador = AnalizadorSintacticoR()
    
    # Analizar el código
    resultado = analizador.analizar(codigo_r)
    
    # Mostrar tokens
    print("\nTokens encontrados:")
    print("-" * 40)
    for token in analizador.tokens:
        print(f"Tipo: {token['tipo']}, Valor: {token['valor']}, Línea: {token['linea']}, Columna: {token['columna']}")
    
    # Mostrar errores sintácticos
    print("\nErrores sintácticos:")
    print("-" * 40)
    if not analizador.errores:
        print("No se encontraron errores sintácticos.")
    else:
        for error in analizador.errores:
            print(f"Línea {error['linea']}, Columna {error['columna']}: {error['mensaje']}")
    
    # Mostrar AST
    print("\nÁrbol Sintáctico (AST):")
    print("-" * 40)
    imprimir_ast(analizador.AST)
    
    return resultado

def imprimir_ast(nodo, nivel=0):
    """
    Imprime el AST de forma jerárquica.
    
    Args:
        nodo: Nodo a imprimir
        nivel: Nivel de indentación
    """
    print("  " * nivel + str(nodo.valor))
    for hijo in nodo.children:
        imprimir_ast(hijo, nivel + 1)

if __name__ == "__main__":
    resultado = main()
    print("\nResultado del análisis:", "Exitoso" if resultado else "Con errores")