import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
# import integracion_trapecio_funcion # Importamos el módulo que contiene la lógica del Trapecio
from integracion_numerical_app.core import trapeze_function_method as integracion_trapecio_funcion

# --- Funciones de la GUI ---

def calcular_integral_trapecio():
    """
    Se ejecuta cuando el usuario presiona el botón 'Calcular'.
    Toma los valores de los campos de entrada, llama a trapecio_funcion,
    y muestra los resultados o errores en la GUI.
    """
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

    try:
        # Validar y convertir entradas
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

        # Llamar a la función de cálculo importada
        resultado_integral, detalles_str = integracion_trapecio_funcion.trapecio_funcion(funcion_str, a, b, N)

        # Mostrar resultados
        text_resultado_integral.config(state=tk.NORMAL)
        text_resultado_integral.insert(tk.END, f"{resultado_integral:.8f}")
        text_resultado_integral.config(state=tk.DISABLED)

        text_detalles_calculo.config(state=tk.NORMAL)
        text_detalles_calculo.insert(tk.END, detalles_str.replace("\\n", "\n")) # Ajustar saltos de línea
        text_detalles_calculo.config(state=tk.DISABLED)

    except ValueError as ve:
        messagebox.showerror("Error de Validación", str(ve))
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")


# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Calculadora de Integrales por Método del Trapecio")
root.geometry("700x750") 

# Estilo
style = ttk.Style(root)
style.theme_use('clam') 

# Frame principal
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(expand=True, fill=tk.BOTH)

# --- Título ---
label_titulo_app = ttk.Label(main_frame, text="Calculadora de Integrales (Método del Trapecio)", font=("Arial", 16, "bold"))
label_titulo_app.pack(pady=(0,15))

# --- Sección de Entradas ---
frame_entradas = ttk.LabelFrame(main_frame, text="Parámetros de Entrada", padding="10 10 10 10")
frame_entradas.pack(fill=tk.X, pady=10)

frame_entradas.columnconfigure(0, weight=1)
frame_entradas.columnconfigure(1, weight=3)

# Función f(x)
label_funcion = ttk.Label(frame_entradas, text="Función f(x):")
label_funcion.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_funcion = ttk.Entry(frame_entradas, width=50)
entry_funcion.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
entry_funcion.insert(0, "x**3 * math.log(x)") # Ejemplo

# Límite inferior a
label_a = ttk.Label(frame_entradas, text="Límite inferior (a):")
label_a.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_a = ttk.Entry(frame_entradas, width=20)
entry_a.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
entry_a.insert(0, "1") # Ejemplo

# Límite superior b
label_b = ttk.Label(frame_entradas, text="Límite superior (b):")
label_b.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_b = ttk.Entry(frame_entradas, width=20)
entry_b.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
entry_b.insert(0, "3") # Ejemplo

# Número de subintervalos N
label_N = ttk.Label(frame_entradas, text="Número de subintervalos (N >= 1):")
label_N.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_N = ttk.Entry(frame_entradas, width=20)
entry_N.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
entry_N.insert(0, "100") # Ejemplo

# --- Botón de Cálculo ---
boton_calcular = ttk.Button(main_frame, text="Calcular Integral (Trapecio)", command=calcular_integral_trapecio, style="Accent.TButton")
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
text_detalles_calculo = scrolledtext.ScrolledText(frame_resultados, height=15, width=80, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 10))
text_detalles_calculo.grid(row=3, column=0, padx=5, pady=(0,5), sticky=tk.NSEW)
frame_resultados.rowconfigure(3, weight=1) 

# --- Instrucciones y Notas ---
frame_notas = ttk.LabelFrame(main_frame, text="Notas", padding="10 10 10 10")
frame_notas.pack(fill=tk.X, pady=10)
label_notas = ttk.Label(frame_notas, 
    text="Funciones matemáticas comunes (sin, cos, exp, log, sqrt, etc.) y constantes (pi, e) están disponibles.\n"
         "Para funciones menos comunes del módulo 'math', use el prefijo 'math.', ej: 'math.gamma(x)'.\n"
         "Asegúrese de que N sea un entero y mayor o igual a 1.", 
    justify=tk.LEFT)
label_notas.pack(padx=5, pady=5, anchor=tk.W)


# --- Iniciar el bucle principal de la GUI ---
if __name__ == "__main__":
    root.mainloop() 