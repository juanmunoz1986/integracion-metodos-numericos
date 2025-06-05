import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
# import integracion_simpson_funcion # Importamos el módulo que contiene la lógica de Simpson
from integracion_numerical_app.core import simpson_function_method as integracion_simpson_funcion
from .graph_utility import plot_function_and_integral # Importar utilidad de graficación

# --- Variables globales para almacenar datos para graficar ---
x_puntos_graf = None
y_puntos_graf = None
resultado_calculado_graf = None

# --- Funciones de la GUI ---

def limpiar_todo():
    """Limpia todos los campos de entrada y salida, y deshabilita el botón de graficar."""
    global x_puntos_graf, y_puntos_graf, resultado_calculado_graf
    entry_funcion.delete(0, tk.END)
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    entry_N.delete(0, tk.END)

    entry_funcion.insert(0, "sin(x)")
    entry_a.insert(0, "0")
    entry_b.insert(0, "3.14159265")
    entry_N.insert(0, "100")

    text_resultado_integral.config(state=tk.NORMAL)
    text_resultado_integral.delete(1.0, tk.END)
    text_resultado_integral.config(state=tk.DISABLED)

    text_detalles_calculo.config(state=tk.NORMAL)
    text_detalles_calculo.delete(1.0, tk.END)
    text_detalles_calculo.config(state=tk.DISABLED)

    boton_graficar.config(state=tk.DISABLED)
    x_puntos_graf = None
    y_puntos_graf = None
    resultado_calculado_graf = None

def calcular_integral():
    """
    Se ejecuta cuando el usuario presiona el botón 'Calcular'.
    Toma los valores de los campos de entrada, llama a simpson_funcion,
    y muestra los resultados o errores en la GUI. Habilita/deshabilita graficación.
    """
    global x_puntos_graf, y_puntos_graf, resultado_calculado_graf

    funcion_str = entry_funcion.get()
    a_str = entry_a.get()
    b_str = entry_b.get()
    N_str = entry_N.get()

    # Limpiar áreas de texto de resultados anteriores
    text_resultado_integral.config(state=tk.NORMAL)
    text_resultado_integral.delete(1.0, tk.END)
    text_resultado_integral.config(state=tk.DISABLED)

    text_detalles_calculo.config(state=tk.NORMAL)
    text_detalles_calculo.delete(1.0, tk.END)
    text_detalles_calculo.config(state=tk.DISABLED)
    
    boton_graficar.config(state=tk.DISABLED) # Deshabilitar por defecto
    x_puntos_graf = None
    y_puntos_graf = None
    resultado_calculado_graf = None

    try:
        if not funcion_str:
            raise ValueError("La función no puede estar vacía.")
        try:
            a = float(a_str)
        except ValueError:
            raise ValueError("El límite inferior 'a' debe ser un número.")
        try:
            b = float(b_str)
        except ValueError:
            raise ValueError("El límite superior 'b' debe ser un número.")
        try:
            N = int(N_str)
        except ValueError:
            raise ValueError("El número de subintervalos 'N' debe ser un entero.")

        # Llamada a la función de lógica que ahora devuelve 4 valores
        # resultado_integral, detalles_str, puntos_x, puntos_y = integracion_simpson_funcion.simpson_funcion(funcion_str, a, b, N)
        retorno_calculo = integracion_simpson_funcion.simpson_funcion(funcion_str, a, b, N)
        
        if not (isinstance(retorno_calculo, tuple) and len(retorno_calculo) == 4):
            messagebox.showerror("Error Interno",
                                 f"La función de cálculo (Simpson Función) no devolvió el formato esperado.\nRecibido: {retorno_calculo}")
            text_detalles_calculo.config(state=tk.NORMAL)
            text_detalles_calculo.insert(tk.END, "Error: Fallo en la comunicación con el núcleo de cálculo.")
            text_detalles_calculo.config(state=tk.DISABLED)
            return
            
        resultado_integral, detalles_str, puntos_x, puntos_y = retorno_calculo

        text_resultado_integral.config(state=tk.NORMAL)
        text_detalles_calculo.config(state=tk.NORMAL)

        if resultado_integral is not None:
            text_resultado_integral.insert(tk.END, f"{resultado_integral:.8f}")
            text_detalles_calculo.insert(tk.END, detalles_str.replace("\\n", "\n"))
            
            x_puntos_graf = puntos_x
            y_puntos_graf = puntos_y
            resultado_calculado_graf = resultado_integral
            boton_graficar.config(state=tk.NORMAL) # Habilitar botón
        else:
            # detalles_str contiene el mensaje de error de la función core
            messagebox.showerror("Error en Cálculo (Simpson Función)", detalles_str)
            text_detalles_calculo.insert(tk.END, f"Error en el cálculo:\n{detalles_str}")

    except ValueError as ve:
        messagebox.showerror("Error de Validación", str(ve))
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {type(e).__name__}: {e}")
    finally:
        text_resultado_integral.config(state=tk.DISABLED)
        text_detalles_calculo.config(state=tk.DISABLED)


def graficar_resultado_actual():
    """Grafica la función y la integral usando los datos del último cálculo exitoso."""
    global x_puntos_graf, y_puntos_graf, resultado_calculado_graf

    if x_puntos_graf is None or y_puntos_graf is None or resultado_calculado_graf is None:
        messagebox.showwarning("Datos Insuficientes", 
                                 "No hay datos suficientes para graficar. Por favor, calcula la integral primero.")
        return

    funcion_str = entry_funcion.get()
    a_str = entry_a.get()
    b_str = entry_b.get()
    N_str = entry_N.get()

    if not all([funcion_str, a_str, b_str, N_str]):
        messagebox.showerror("Error de Entrada", "Faltan datos en los campos para graficar (función, a, b, N).")
        return
    try:
        a = float(a_str)
        b = float(b_str)
        N = int(N_str)
    except ValueError:
        messagebox.showerror("Error de Entrada", "Los valores de a, b, N para graficar no son numéricos.")
        return

    try:
        plot_function_and_integral(
            func_str=funcion_str, 
            a=a, 
            b=b, 
            N=N, 
            result=resultado_calculado_graf,
            x_points_method=x_puntos_graf, 
            y_points_method=y_puntos_graf,
            method_name="Simpson 1/3"
        )
    except Exception as e:
        messagebox.showerror("Error al Graficar", f"Ocurrió un error al generar la gráfica: {e}")


# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Calculadora de Integrales por Simpson 1/3 (Función)")
root.geometry("700x750") # Ajustar tamaño según sea necesario
root.configure(bg='#f0f0f0')

# Estilo
style = ttk.Style(root)
style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
style.configure('.', background='#f0f0f0', font=('Arial', 11)) # Estilo base, fuente para labels
style.configure('TEntry', font=('Arial', 11), padding=5)

# Frame principal para organizar los widgets
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(expand=True, fill=tk.BOTH)

# --- Título ---
label_titulo_app = ttk.Label(main_frame, text="Calculadora de Integrales (Método de Simpson 1/3)", font=("Arial", 16, "bold"))
label_titulo_app.pack(pady=(0,15))

# --- Sección de Entradas ---
frame_entradas = ttk.LabelFrame(main_frame, text="Parámetros de Entrada", padding="10 10 10 10")
frame_entradas.pack(fill=tk.X, pady=10)

# Configurar columnas para que las etiquetas y entradas se alineen bien
frame_entradas.columnconfigure(0, weight=1)
frame_entradas.columnconfigure(1, weight=3)

# Función f(x)
label_funcion = ttk.Label(frame_entradas, text="Función f(x):")
label_funcion.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_funcion = ttk.Entry(frame_entradas, width=50)
entry_funcion.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
entry_funcion.insert(0, "x**2 * math.exp(-x)") # Ejemplo

# Límite inferior a
label_a = ttk.Label(frame_entradas, text="Límite inferior (a):")
label_a.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_a = ttk.Entry(frame_entradas, width=20)
entry_a.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
entry_a.insert(0, "0") # Ejemplo

# Límite superior b
label_b = ttk.Label(frame_entradas, text="Límite superior (b):")
label_b.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_b = ttk.Entry(frame_entradas, width=20)
entry_b.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
entry_b.insert(0, "10") # Ejemplo

# Número de subintervalos N
label_N = ttk.Label(frame_entradas, text="Número de subintervalos (N, par >= 6):")
label_N.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_N = ttk.Entry(frame_entradas, width=20)
entry_N.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
entry_N.insert(0, "100") # Ejemplo

# --- Botón de Cálculo ---
# Contenedor para los botones
frame_botones = ttk.Frame(main_frame)
frame_botones.pack(pady=15)

boton_calcular = ttk.Button(frame_botones, text="Calcular Integral", command=calcular_integral)
boton_calcular.pack(side=tk.LEFT, padx=5)

boton_graficar = ttk.Button(frame_botones, text="Graficar", command=graficar_resultado_actual, state=tk.DISABLED)
boton_graficar.pack(side=tk.LEFT, padx=5)

boton_limpiar_gui = ttk.Button(frame_botones, text="Limpiar", command=limpiar_todo)
boton_limpiar_gui.pack(side=tk.LEFT, padx=5)


# --- Sección de Resultados ---
frame_resultados = ttk.LabelFrame(main_frame, text="Resultados", padding="10 10 10 10")
frame_resultados.pack(fill=tk.BOTH, expand=True, pady=10)
frame_resultados.columnconfigure(0, weight=1) # Para que el ScrolledText se expanda

# Resultado de la Integral
label_resultado_integral = ttk.Label(frame_resultados, text="Aproximación de la Integral:")
label_resultado_integral.grid(row=0, column=0, padx=5, pady=(5,0), sticky=tk.W)
text_resultado_integral = scrolledtext.ScrolledText(frame_resultados, height=2, width=60, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 10), background='#ffffff')
text_resultado_integral.grid(row=1, column=0, padx=5, pady=(0,10), sticky=tk.EW)

# Detalles del Cálculo
label_detalles_calculo = ttk.Label(frame_resultados, text="Detalles del Cálculo:")
label_detalles_calculo.grid(row=2, column=0, padx=5, pady=(5,0), sticky=tk.W)
text_detalles_calculo = scrolledtext.ScrolledText(frame_resultados, height=15, width=80, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 10), background='#ffffff')
text_detalles_calculo.grid(row=3, column=0, padx=5, pady=(0,5), sticky=tk.NSEW)
frame_resultados.rowconfigure(3, weight=1) # Para que el ScrolledText de detalles se expanda

# --- Instrucciones y Notas ---
frame_notas = ttk.LabelFrame(main_frame, text="Notas", padding="10 10 10 10")
frame_notas.pack(fill=tk.X, pady=10)
label_notas = ttk.Label(frame_notas, 
    text="Funciones matemáticas comunes (sin, cos, exp, log, sqrt, etc.) y constantes (pi, e) están disponibles.\n"
         "Para funciones menos comunes del módulo 'math', use el prefijo 'math.', ej: 'math.gamma(x)'.\n"
         "Asegúrese de que N sea un número par y mayor o igual a 6.", 
    justify=tk.LEFT)
label_notas.pack(padx=5, pady=5, anchor=tk.W)


# --- Iniciar el bucle principal de la GUI ---
if __name__ == "__main__":
    # Inicializar estado del botón graficar al inicio
    if boton_graficar: # Asegurarse que el widget existe
        boton_graficar.config(state=tk.DISABLED)
    root.mainloop() 