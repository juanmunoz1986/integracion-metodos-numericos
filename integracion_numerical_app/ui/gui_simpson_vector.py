import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
# import integracion_simpson # Importamos el módulo que contiene la lógica de Simpson con vectores
from integracion_numerical_app.core import simpson_vector_method as integracion_simpson

# --- Funciones de la GUI ---

def parse_vector_input(input_str, vector_name):
    """Convierte una cadena de entrada (ej: "1, 2.5, 3") en una lista de floats."""
    if not input_str.strip():
        raise ValueError(f"La entrada para el vector '{vector_name}' no puede estar vacía.")
    try:
        # Reemplazar comas por espacios, luego dividir y convertir a float
        vector = [float(elem) for elem in input_str.replace(",", " ").split()]
        return vector
    except ValueError:
        raise ValueError(f"Entrada inválida para el vector '{vector_name}'. Asegúrese de que todos los elementos sean números válidos (ej: 1 o 2.3) separados por comas o espacios.")

def calcular_integral_simpson_vectores():
    """
    Se ejecuta cuando el usuario presiona el botón 'Calcular'.
    Toma los valores de los campos de entrada, los parsea, llama a simpson_un_tercio,
    y muestra los resultados o errores en la GUI.
    """
    x_str = entry_x_valores.get()
    fx_str = entry_fx_valores.get()

    # Limpiar áreas de texto de resultados anteriores
    text_resultado_integral.config(state=tk.NORMAL)
    text_resultado_integral.delete(1.0, tk.END)
    text_resultado_integral.config(state=tk.DISABLED)

    text_detalles_calculo.config(state=tk.NORMAL)
    text_detalles_calculo.delete(1.0, tk.END)
    text_detalles_calculo.config(state=tk.DISABLED)

    try:
        x_valores = parse_vector_input(x_str, "x")
        fx_valores = parse_vector_input(fx_str, "f(x)")

        # Llamar a la función de cálculo importada
        resultado_integral, detalles_str = integracion_simpson.simpson_un_tercio(x_valores, fx_valores)

        # Mostrar resultados
        text_resultado_integral.config(state=tk.NORMAL)
        text_resultado_integral.insert(tk.END, f"{resultado_integral:.8f}")
        text_resultado_integral.config(state=tk.DISABLED)

        text_detalles_calculo.config(state=tk.NORMAL)
        # El detalle_str de integracion_simpson.py ya usa \\n, así que lo reemplazamos por \n para tkinter
        text_detalles_calculo.insert(tk.END, detalles_str.replace("\\n", "\n"))
        text_detalles_calculo.config(state=tk.DISABLED)

    except ValueError as ve:
        messagebox.showerror("Error de Validación o Cálculo", str(ve))
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")


# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Calculadora de Integrales por Simpson 1/3 (Vectores)")
root.geometry("700x650") # Ajustar altura según necesidad

# Estilo
style = ttk.Style(root)
style.theme_use('clam')

# Frame principal
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(expand=True, fill=tk.BOTH)

# --- Título ---
label_titulo_app = ttk.Label(main_frame, text="Calculadora de Integrales (Simpson 1/3 con Vectores)", font=("Arial", 16, "bold"))
label_titulo_app.pack(pady=(0,15))

# --- Sección de Entradas ---
frame_entradas = ttk.LabelFrame(main_frame, text="Datos de Entrada (Vectores)", padding="10 10 10 10")
frame_entradas.pack(fill=tk.X, pady=10)

frame_entradas.columnconfigure(0, weight=1) # Etiqueta
frame_entradas.columnconfigure(1, weight=3) # Campo de entrada

# Valores de x
label_x_valores = ttk.Label(frame_entradas, text="Valores de x (separados por comas/espacios):")
label_x_valores.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_x_valores = ttk.Entry(frame_entradas, width=60)
entry_x_valores.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
entry_x_valores.insert(0, "0, 0.25, 0.5, 0.75, 1.0") # Ejemplo

# Valores de f(x)
label_fx_valores = ttk.Label(frame_entradas, text="Valores de f(x) (separados por comas/espacios):")
label_fx_valores.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_fx_valores = ttk.Entry(frame_entradas, width=60)
entry_fx_valores.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
entry_fx_valores.insert(0, "1.0, 0.939, 0.778, 0.569, 0.367") # Ejemplo f(x) = exp(-x) para los x de arriba

# --- Botón de Cálculo ---
boton_calcular = ttk.Button(main_frame, text="Calcular Integral (Simpson Vectores)", command=calcular_integral_simpson_vectores, style="Accent.TButton")
boton_calcular.pack(pady=15)
style.configure("Accent.TButton", font=("Arial", 12, "bold"), padding=10)

# --- Sección de Resultados ---
frame_resultados = ttk.LabelFrame(main_frame, text="Resultados", padding="10 10 10 10")
frame_resultados.pack(fill=tk.BOTH, expand=True, pady=10)
frame_resultados.columnconfigure(0, weight=1)

# Resultado de la Integral
label_resultado_integral = ttk.Label(frame_resultados, text="Aproximación de la Integral:")
label_resultado_integral.grid(row=0, column=0, padx=5, pady=(5,0), sticky=tk.W)
text_resultado_integral = scrolledtext.ScrolledText(frame_resultados, height=2, width=60, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 10))
text_resultado_integral.grid(row=1, column=0, padx=5, pady=(0,10), sticky=tk.EW)

# Detalles del Cálculo
label_detalles_calculo = ttk.Label(frame_resultados, text="Detalles del Cálculo:")
label_detalles_calculo.grid(row=2, column=0, padx=5, pady=(5,0), sticky=tk.W)
text_detalles_calculo = scrolledtext.ScrolledText(frame_resultados, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 10))
text_detalles_calculo.grid(row=3, column=0, padx=5, pady=(0,5), sticky=tk.NSEW)
frame_resultados.rowconfigure(3, weight=1)

# --- Instrucciones y Notas ---
frame_notas = ttk.LabelFrame(main_frame, text="Notas Importantes", padding="10 10 10 10")
frame_notas.pack(fill=tk.X, pady=10)
label_notas_texto = (
    "- Ingrese los valores numéricos para 'x' y 'f(x)' separados por comas y/o espacios.\n"
    "- Los valores de 'x' deben estar equiespaciados y en orden ascendente.\n"
    "- El número total de puntos (pares x, f(x)) debe ser IMPAR y al menos 3.\n"
    "  (Esto significa un número PAR de subintervalos, N >= 2)."
)
label_notas = ttk.Label(frame_notas, text=label_notas_texto, justify=tk.LEFT)
label_notas.pack(padx=5, pady=5, anchor=tk.W)

# --- Iniciar el bucle principal de la GUI ---
if __name__ == "__main__":
    root.mainloop() 