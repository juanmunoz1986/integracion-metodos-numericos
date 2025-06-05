import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
import re # Importar re para expresiones regulares
# Asegúrate de que la ruta de importación sea correcta según tu estructura.
# Si ejecutas gradio_app.py desde la raíz del proyecto, esta importación debería funcionar.
# from integracion_numerical_app.core.trapezoid_function_method import trapecio_funcion 
# O si el archivo correcto es trapeze_function_method.py:
from integracion_numerical_app.core.trapeze_function_method import trapecio_funcion

# Namespace para la evaluación segura de la función ingresada por el usuario.
# Es una buena práctica tener esto bien definido y posiblemente importarlo si es complejo.
_SAFE_DICT_GRADIO = {
    "np": np,
    # Permite al usuario escribir math.func y se mapeará a np.func
    "math": np, 
    "sin": np.sin, "cos": np.cos, "tan": np.tan, "log": np.log, "exp": np.exp, "sqrt": np.sqrt,
    "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan, "arctan2": np.arctan2,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
    "arcsinh": np.arcsinh, "arccosh": np.arccosh, "arctanh": np.arctanh,
    "degrees": np.degrees, "radians": np.radians,
    "pi": np.pi, "e": np.e, "inf": np.inf, "nan": np.nan,
    "abs": np.abs, "fabs": np.fabs, "floor": np.floor, "ceil": np.ceil, "pow": np.power,
    # 'x' se añadirá dinámicamente al diccionario antes de la llamada a eval()
}

# START NEW HELPER FUNCTION
def formatear_detalles_a_markdown(detalles_str):
    """
    Convierte la cadena de detalles del cálculo a formato Markdown.
    """
    if not detalles_str:
        return "No hay detalles disponibles."

    # Reemplazar dobles barras invertidas \n (que son \n en la cadena) por <br> para saltos de línea HTML
    # Esto es más robusto en Markdown para asegurar saltos de línea donde se esperan.
    md_str = detalles_str.replace("\\n", "<br>") # Corregido para reemplazar la secuencia literal \n

    # Formatear la tabla de puntos
    # Buscar la sección de la tabla
    tabla_match = re.search(r"(Tabla de evaluación de la función en los puntos:<br>)(Índice.*?)(<br><br>Suma completa)", md_str, re.DOTALL)
    
    if tabla_match:
        prefijo_tabla = tabla_match.group(1)
        contenido_tabla_bruto = tabla_match.group(2)
        sufijo_tabla = tabla_match.group(3)

        lineas_tabla = contenido_tabla_bruto.strip().split("<br>")
        
        tabla_markdown = prefijo_tabla # Mantener el título de la tabla
        
        if len(lineas_tabla) > 1: # Encabezado y al menos una línea de separador/datos
            # Encabezado
            encabezado = lineas_tabla[0].strip()
            # Limpiar y asegurar que sea una fila de tabla Markdown
            columnas_encabezado = [col.strip() for col in encabezado.split('|')]
            tabla_markdown += f"| {' | '.join(columnas_encabezado)} |<br>" # Añadir pipes al inicio/final si no están
            
            # Separador Markdown (ajustar número de columnas si es necesario)
            num_cols = len(columnas_encabezado)
            tabla_markdown += f"|{'---|' * num_cols}<br>"
            
            # Filas de datos (desde la línea 2, asumiendo que la línea 1 es el separador "---")
            for linea_datos in lineas_tabla[2:]: # Saltar la línea de "-------"
                linea_datos = linea_datos.strip()
                if not linea_datos or linea_datos.startswith("----"): # Ignorar líneas vacías o separadores extra
                    continue
                columnas_datos = [col.strip() for col in linea_datos.split('|')]
                tabla_markdown += f"| {' | '.join(columnas_datos)} |<br>"
            
            # Recomponer la cadena con la tabla formateada
            md_str = tabla_markdown + sufijo_tabla
        else: # Si la tabla no tiene el formato esperado, mostrarla tal cual (ya con <br>)
            md_str = prefijo_tabla + contenido_tabla_bruto + sufijo_tabla
            
    # Envolver la sección de "Suma completa" en un bloque de código para preservar el formato
    # o simplemente asegurar que los <br> hagan su trabajo.
    # Por ahora, los <br> deberían ser suficientes para la legibilidad de las sumas.

    # Añadir algunos encabezados Markdown para mejorar la estructura general
    md_str = md_str.replace("Método del Trapecio", "### Método del Trapecio")
    md_str = md_str.replace("Cálculo de h:", "#### Cálculo de h:")
    md_str = md_str.replace("Tabla de evaluación de la función en los puntos:", "#### Tabla de evaluación de la función en los puntos:")
    md_str = md_str.replace("Suma completa (según la fórmula del Trapecio):", "#### Suma completa (según la fórmula del Trapecio):")
    
    return md_str
# END NEW HELPER FUNCTION

def calcular_y_graficar_trapecio_gradio(func_str_usuario, limite_a, limite_b, num_intervalos):
    """
    Función principal para la interfaz de Gradio.
    Calcula la integral, genera la gráfica y devuelve los resultados.
    """
    if not all([func_str_usuario, limite_a is not None, limite_b is not None, num_intervalos is not None]):
        # Devolver mensaje de error para ambos outputs si es un error de validación temprano
        return "Error: Todos los campos son obligatorios.", None 
    try:
        a = float(limite_a)
        b = float(limite_b)
        N = int(num_intervalos)
    except ValueError:
        return "Error: Los límites 'a', 'b' y el número 'N' deben ser numéricos.", None

    if N <= 0:
        return "Error: 'N' debe ser un entero positivo.", None
    if a >= b:
        return "Error: El límite 'a' debe ser menor que 'b'.", None

    # Limpiar la figura de Matplotlib al inicio de cada llamada para evitar superposiciones
    plt.clf()
    fig, ax = plt.subplots()

    try:
        # 1. Calcular la integral usando la función del core
        # Asumo que trapecio_funcion devuelve: resultado, detalles_str, x_puntos_metodo, y_puntos_metodo
        integral_valor, detalles_calculo_bruto, x_metodo, y_metodo = trapecio_funcion(func_str_usuario, a, b, N)

        # Formatear detalles para Markdown ANTES de usarlos o devolverlos
        detalles_formateados_md = formatear_detalles_a_markdown(detalles_calculo_bruto)

        # Si la función del core devuelve None para integral_valor, indica un error en el cálculo
        if integral_valor is None:
            # El error ya debería estar en detalles_formateados_md (proveniente de trapecio_funcion)
            # Mostrar el mensaje de error en el área de texto y en la gráfica
            ax.text(0.5, 0.5, detalles_formateados_md if detalles_formateados_md else "Error en el cálculo del método.", 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, color='red', bbox=dict(boxstyle="round,pad=0.3", fc="pink", alpha=0.8))
            ax.set_title("Error en Cálculo del Método")
            return detalles_formateados_md, fig # Devolver el error formateado y la figura con el error

        # 2. Preparar la gráfica
        # Evaluar la función del usuario para una curva suave
        x_curva = np.linspace(a, b, max(200, N * 5)) # Puntos para la curva
        
        y_curva = None
        error_eval_func = ""
        try:
            # Reemplazar ^ con ** para la exponenciación si es necesario para eval
            processed_func_str = func_str_usuario.replace('^', '**')
            
            # Crear el diccionario de evaluación para la función del usuario
            # Es importante que 'x' esté disponible aquí.
            # No se debe modificar _SAFE_DICT_GRADIO directamente si se reutiliza.
            eval_globals = {"__builtins__": {}}
            eval_locals = {**_SAFE_DICT_GRADIO, "x": x_curva} # Añadir x_curva para la evaluación
            
            y_curva = eval(processed_func_str, eval_globals, eval_locals)
        except Exception as e_func:
            error_eval_func = f"Error al evaluar f(x) para graficar: {type(e_func).__name__}: {str(e_func)}"
        
        if y_curva is not None:
            ax.plot(x_curva, y_curva, 'b-', label=f'f(x) = {func_str_usuario}', linewidth=2)
            ax.fill_between(x_curva, y_curva, where=((x_curva >= a) & (x_curva <= b)), color='skyblue', alpha=0.4, label='Área de la integral')
        else:
            ax.text(0.5, 0.5, error_eval_func, horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, color='red', bbox=dict(boxstyle="round,pad=0.3", fc="wheat", alpha=0.8))

        # Graficar los puntos y líneas del método del trapecio
        if x_metodo is not None and y_metodo is not None and len(x_metodo) > 0:
            x_metodo_np = np.array(x_metodo)
            y_metodo_np = np.array(y_metodo)
            ax.plot(x_metodo_np, y_metodo_np, 'ro-', label=f'Aproximación ({N} trapecios)', markersize=4)
            for i in range(len(x_metodo_np) - 1):
                ax.plot([x_metodo_np[i], x_metodo_np[i+1]], [y_metodo_np[i], y_metodo_np[i+1]], 'g--', linewidth=1)
        
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        title_string = f"Integral (Trapecio): {integral_valor:.7f}" if integral_valor is not None else "Integral (Trapecio): Error en Cálculo"
        ax.set_title(title_string)
        ax.legend(loc='upper left', bbox_to_anchor=(0, -0.15)) # Ajustar un poco más la leyenda si es necesario
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        plt.tight_layout(rect=[0, 0.05, 1, 1]) # Ajustar layout para que la leyenda no se corte
        
        # Construir el texto de salida principal con el resultado numérico
        salida_texto_principal = f"### Resultado de la Integral\n**Valor aproximado: {integral_valor:.8f}**\n\n"
        
        # Combinar con los detalles formateados
        salida_markdown_completa = salida_texto_principal + detalles_formateados_md
        
        return salida_markdown_completa, fig

    except Exception as e:
        # Captura errores de trapecio_funcion o cualquier otro imprevisto
        error_msg_general = f"Error general en el proceso: {type(e).__name__}: {str(e)}"
        # Mostrar error en la gráfica también si es posible
        ax.text(0.5, 0.5, error_msg_general, horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, color='red', bbox=dict(boxstyle="round,pad=0.3", fc="pink", alpha=0.8))
        ax.set_title("Error en la Operación")
        # Devolver el error formateado para que se muestre en el área de Markdown
        return f"### Error\n{error_msg_general}", fig


# Crear la interfaz Gradio
iface = gr.Interface(
    fn=calcular_y_graficar_trapecio_gradio,
    inputs=[
        gr.Textbox(label="Función f(x) (ej. x**2 * np.sin(x) o x**3 * math.log(x))", value="x**3 * math.log(x)"),
        gr.Number(label="Límite inferior (a)", value=1.0),
        gr.Number(label="Límite superior (b)", value=3.0),
        gr.Number(label="Número de subintervalos (N >=1)", value=100, minimum=1, precision=0) # precision=0 para entero
    ],
    outputs=[
        gr.Markdown(label="Resultado y Detalles"), # MODIFICADO: Usar gr.Markdown
        gr.Plot(label="Gráfica de la Función e Integral")
    ],
    title="Calculadora de Integrales con Gradio - Método del Trapecio",
    description="Ingresa una función en términos de 'x'. Puedes usar funciones de 'np' o 'math' (ej. np.sin(x), math.log(x)). La sintaxis de Python es esperada (ej. '**' para potencias).",
    allow_flagging='never',
    examples=[
        ["np.sin(x)", 0, np.pi, 50],
        ["x**2", 0, 1, 100],
        ["math.exp(-x**2)", -1, 1, 200],
        ["1/(1+x**2)", -5, 5, 100],
        ["x**3 * math.log(x)", 1, 3, 100]
    ],
    article="""
    ### Notas de Uso:
    - La variable independiente debe ser 'x'.
    - Para funciones matemáticas, usa prefijo `np.` o `math.` (ej. `np.sin(x)`, `math.log(x)`). Ambos se resuelven a funciones de NumPy.
    - La potencia es `**` (ej. `x**2` para x al cuadrado).
    - Asegúrate de que el límite inferior 'a' sea menor que el límite superior 'b'.
    - 'N' debe ser al menos 1.
    """
)

if __name__ == '__main__':
    # Añadir el directorio del proyecto al PYTHONPATH para asegurar que el paquete sea encontrable
    # Esto es crucial si ejecutas 'python gradio_app.py' desde la raíz y 'integracion_numerical_app' es un paquete local.
    import sys
    import os
    project_root = os.path.dirname(os.path.abspath(__file__))
    # Si 'integracion_numerical_app' está en el mismo directorio que 'gradio_app.py',
    # y 'gradio_app.py' está en la raíz, entonces el project_root es la raíz.
    # Si 'integracion_numerical_app' es un subdirectorio, y es un paquete,
    # la importación 'from integracion_numerical_app.core...' debería funcionar si la raíz está en PYTHONPATH.
    # Lo siguiente es una forma robusta de asegurar que 'integracion_numerical_app' (si está en la raíz como módulo) se pueda importar.
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Verificar que la importación funciona o ajustar según sea necesario
    try:
        from integracion_numerical_app.core.trapeze_function_method import trapecio_funcion
        print("Importación de 'trapecio_funcion' desde trapeze_function_method.py exitosa.")
    except ModuleNotFoundError:
        print("Error: No se pudo importar 'trapecio_funcion'. Verifica la ruta de importación y la estructura del proyecto.")
        print("PYTHONPATH actual:", sys.path)
        print("Asegúrate de que 'integracion_numerical_app' sea accesible.")
        # Si tienes 'integracion_numerical_app' como un paquete en la raíz, la importación debería funcionar
        # si ejecutas python -m nombre_del_paquete_principal.gradio_app o similar,
        # o si la raíz está en PYTHONPATH.
        # Para una ejecución simple 'python gradio_app.py' desde la raíz,
        # y si 'integracion_numerical_app' es un directorio en la raíz con un __init__.py,
        # la importación 'from integracion_numerical_app...' debería funcionar.

    iface.launch() 