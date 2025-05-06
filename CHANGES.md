# Mejoras al Compilador para R

## Mejoras al Analizador Semántico

### 1. Seguimiento de Variables Declaradas
- Se agregó un diccionario `variables_declaradas` para rastrear las variables declaradas y sus tipos.
- Esto permite detectar el uso de variables no declaradas en diferentes contextos.

### 2. Verificación de Tipos
- Se implementó la verificación de compatibilidad de tipos en operaciones.
- Se verifica que los operadores de comparación numérica (<, >, >=, <=) se usen con operandos numéricos.
- Se verifica que las comparaciones de igualdad (==) se realicen entre tipos compatibles.

### 3. Verificación de Variables en Expresiones
- Se agregó la capacidad de detectar variables no declaradas en expresiones aritméticas.
- Se analiza cada token en una expresión para verificar si las variables están declaradas.

### 4. Verificación de Sentencias
- Se mejoró la verificación de sentencias if, print y switch.
- Se verifica que las variables usadas en condiciones, impresiones y casos de switch estén declaradas.

### 5. Mejora en Reportes de Errores
- Se agregó información de línea y columna a los mensajes de error semántico.
- Esto facilita la localización y corrección de errores.

### 6. Integración con la GUI
- Se implementó la funcionalidad del analizador semántico en la interfaz gráfica.
- Se agregó un comando al menú para realizar análisis semántico.
- Se muestra información sobre variables declaradas y errores semánticos en la salida.

## Cómo Usar el Analizador Semántico

1. Escriba su código R en el editor.
2. Vaya al menú "Compiladores" y seleccione "Analizador Semántico".
3. El analizador mostrará las variables declaradas y cualquier error semántico encontrado.

## Errores Semánticos Detectados

El analizador semántico puede detectar los siguientes tipos de errores:

- Uso de variables no declaradas
- Incompatibilidad de tipos en operaciones
- Sentencias incompletas o mal formadas
- Condiciones if incompletas
- Sentencias print incorrectas
- Sentencias switch incompletas