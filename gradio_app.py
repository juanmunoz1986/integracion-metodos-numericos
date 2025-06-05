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

# START NEW HELPER FUNCTIONS
def _formatear_seccion_principal_markdown(seccion_bruta_str):
    md_str = seccion_bruta_str.replace("\\n", "<br>")
    
    tabla_match = re.search(r"(Tabla de evaluación de la función en los puntos:<br>)(.*?)(<br><br>|$)", md_str, re.DOTALL)
    if tabla_match:
        prefijo_tabla = tabla_match.group(1)
        contenido_tabla_bruto = tabla_match.group(2)
        sufijo_tabla = tabla_match.group(3)

        lineas_tabla_brutas = contenido_tabla_bruto.strip().split("<br>")
        tabla_markdown_interna = ""
        
        if len(lineas_tabla_brutas) > 1: # Debe haber encabezado y al menos el separador original
            encabezado_original = lineas_tabla_brutas[0].strip()
            columnas_encabezado_raw = [col.strip() for col in encabezado_original.split('|')]
            columnas_encabezado = [c for c in columnas_encabezado_raw if c]
            if columnas_encabezado:
                tabla_markdown_interna += f"| {' | '.join(columnas_encabezado)} |<br>"
                num_cols = len(columnas_encabezado)
                tabla_markdown_interna += f"|{'---:|' * num_cols}<br>"

                # Procesar filas de datos (saltando encabezado original y su línea '---')
                for linea_datos_str in lineas_tabla_brutas[2:]: 
                    linea_datos_str = linea_datos_str.strip()
                    if not linea_datos_str or linea_datos_str.startswith("----"): continue
                    columnas_datos_raw = [col.strip() for col in linea_datos_str.split('|')]
                    columnas_datos = [c for c in columnas_datos_raw if c] 
                    if columnas_datos:
                        tabla_markdown_interna += f"| {' | '.join(columnas_datos)} |<br>"
            
            md_str = prefijo_tabla + tabla_markdown_interna + sufijo_tabla
    
    md_str = md_str.replace("Método del Trapecio", "### Método del Trapecio")
    md_str = md_str.replace("Cálculo de h:", "#### Cálculo de h:")
    # El título "Tabla de evaluación..." ya está en prefijo_tabla
    return md_str.strip()

def _formatear_seccion_suma_markdown(seccion_bruta_str):
    if not seccion_bruta_str or not seccion_bruta_str.strip():
        return "_No se generaron detalles de la suma._"
    
    # El título "Suma completa..." ya está incluido en seccion_bruta_str desde la división
    md_output = "### Desglose de la Suma (Método del Trapecio)\n"
    md_output += "```text\n"
    suma_limpia = seccion_bruta_str.replace("\\n", "\n").strip()
    md_output += suma_limpia
    md_output += "\n```"
    return md_output
# END NEW HELPER FUNCTIONS

def calcular_y_graficar_trapecio_gradio(func_str_usuario, limite_a, limite_b, num_intervalos):
    """
    Función principal para la interfaz de Gradio.
    Calcula la integral, genera la gráfica y devuelve los resultados.
    """
    if not all([func_str_usuario, limite_a is not None, limite_b is not None, num_intervalos is not None]):
        # Devolver mensaje de error para ambos outputs si es un error de validación temprano
        return "Error: Todos los campos son obligatorios.", None, "_Error en cálculo, no hay desglose de suma disponible._"
    try:
        a = float(limite_a)
        b = float(limite_b)
        N = int(num_intervalos)
    except ValueError:
        return "Error: Los límites 'a', 'b' y el número 'N' deben ser numéricos.", None, "_Error en cálculo, no hay desglose de suma disponible._"

    if N <= 0:
        return "Error: 'N' debe ser un entero positivo.", None, "_Error en cálculo, no hay desglose de suma disponible._"
    if a >= b:
        return "Error: El límite 'a' debe ser menor que 'b'.", None, "_Error en cálculo, no hay desglose de suma disponible._"

    # Limpiar la figura de Matplotlib al inicio de cada llamada para evitar superposiciones
    plt.clf()
    fig, ax = plt.subplots()

    try:
        # 1. Calcular la integral usando la función del core
        # Asumo que trapecio_funcion devuelve: resultado, detalles_str, x_puntos_metodo, y_puntos_metodo
        integral_valor, detalles_calculo_bruto, x_metodo, y_metodo = trapecio_funcion(func_str_usuario, a, b, N)

        # Formatear detalles para Markdown ANTES de usarlos o devolverlos
        detalles_formateados_md = _formatear_seccion_principal_markdown(detalles_calculo_bruto)

        # Si la función del core devuelve None para integral_valor, indica un error en el cálculo
        if integral_valor is None:
            # El error ya debería estar en detalles_formateados_md (proveniente de trapecio_funcion)
            # Mostrar el mensaje de error en el área de texto y en la gráfica
            ax.text(0.5, 0.5, detalles_formateados_md if detalles_formateados_md else "Error en el cálculo del método.", 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, color='red', bbox=dict(boxstyle="round,pad=0.3", fc="pink", alpha=0.8))
            ax.set_title("Error en Cálculo del Método")
            return f"### Error en Cálculo<br>{detalles_formateados_md}", fig, "_Error en cálculo, no hay desglose de suma disponible._"

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
        md_principal_final = salida_texto_principal + detalles_formateados_md
        
        # Dividir detalles_calculo_bruto en sección principal y sección de suma
        partes_detalles = detalles_calculo_bruto.split("Suma completa (según la fórmula del Trapecio):", 1)
        seccion_principal_bruta = partes_detalles[0]
        seccion_suma_bruta = ""
        if len(partes_detalles) > 1:
            seccion_suma_bruta = "Suma completa (según la fórmula del Trapecio):" + partes_detalles[1]

        md_suma_completa = _formatear_seccion_suma_markdown(seccion_suma_bruta)
        
        return md_principal_final, fig, md_suma_completa

    except Exception as e:
        # Captura errores de trapecio_funcion o cualquier otro imprevisto
        error_msg_general = f"Error general en el proceso: {type(e).__name__}: {str(e)}"
        # Mostrar error en la gráfica también si es posible
        ax.text(0.5, 0.5, error_msg_general, horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, color='red', bbox=dict(boxstyle="round,pad=0.3", fc="pink", alpha=0.8))
        ax.set_title("Error en la Operación")
        # Devolver el error formateado para que se muestre en el área de Markdown
        return f"### Error<br>{error_msg_general}", fig, f"_Error general, no hay desglose de suma: {error_msg_general}_"

# MODIFICACIÓN PRINCIPAL: Usar gr.Blocks para el layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## Calculadora de Integrales con Gradio - Método del Trapecio")
    gr.Markdown("Ingresa una función en términos de 'x'. Puedes usar funciones de 'np' o 'math' (ej. np.sin(x), math.log(x)). La sintaxis de Python es esperada (ej. '**' para potencias).")
    
    with gr.Row():
        with gr.Column(scale=1): # Columna de Entradas
            input_funcion = gr.Textbox(label="Función f(x) (ej. x**2)", value="e**x**2")
            input_a = gr.Number(label="Límite inferior (a)", value=0)
            input_b = gr.Number(label="Límite superior (b)", value=1)
            input_N = gr.Number(label="Número de subintervalos (N >=1)", value=10, minimum=1, precision=0)
            
            with gr.Row():
                btn_clear = gr.Button("Clear")
                btn_submit = gr.Button("Submit", variant="primary")
                
        with gr.Column(scale=2): # Columna de Salidas (más ancha)
            output_principal_md = gr.Markdown(label="Resultado y Detalles de Evaluación")
            output_plot = gr.Plot(label="Gráfica de la Función e Integral")
            output_suma_md = gr.Markdown(label="Desglose de la Suma (Método del Trapecio)")

    # Acciones de los botones
    btn_submit.click(
        fn=calcular_y_graficar_trapecio_gradio,
        inputs=[input_funcion, input_a, input_b, input_N],
        outputs=[output_principal_md, output_plot, output_suma_md]
    )
    
    # Acción del botón Clear (limpia todos los campos de entrada y salida)
    all_inputs = [input_funcion, input_a, input_b, input_N]
    all_outputs = [output_principal_md, output_plot, output_suma_md]
    
    def clear_fields():
        # Para los inputs, los reseteamos a un valor por defecto o vacío
        # Para los outputs, los reseteamos a None o un string vacío
        return ["e**x**2", 0, 1, 10, # Valores por defecto para inputs
                None, None, None] # None para outputs los limpiará
                
    btn_clear.click(fn=clear_fields, inputs=None, outputs=all_inputs + all_outputs)

    # Definir ejemplos (esto es un poco diferente con Blocks)
    gr.Examples(
        examples=[
            ["np.sin(x)", 0, np.pi, 50],
            ["x**2", 0, 1, 100],
            ["math.exp(-x**2)", -1, 1, 200],
            ["1/(1+x**2)", -5, 5, 100],
            ["x**3 * math.log(x)", 1, 3, 100]
        ],
        inputs=all_inputs # Los ejemplos se aplicarán a estos inputs
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

    demo.launch() 