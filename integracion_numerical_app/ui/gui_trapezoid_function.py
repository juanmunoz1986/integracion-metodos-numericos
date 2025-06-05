import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ..core.trapeze_function_method import trapecio_funcion
from .graph_utility import plot_function_and_integral

class CalculadoraTrapecioUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Integrales - Método del Trapecio (Función)") 
        self.root.geometry("650x650")
        self.root.configure(bg='#f0f0f0')

        self.x_puntos_graf = None
        self.y_puntos_graf = None
        self.resultado_calculado = None

        main_frame = ttk.Frame(root, padding="20") # No necesita estilo 'Main.TFrame' si es solo fondo
        main_frame.pack(expand=True, fill=tk.BOTH)
        # main_frame.master.configure(bg='#f0f0f0') # El root ya tiene este bg

        style = ttk.Style(self.root)
        style.theme_use('clam') 

        # Estilos generales que no afectan a los botones directamente
        style.configure('.', background='#f0f0f0') # Estilo base para todos los widgets ttk
        style.configure('TLabel', font=('Arial', 11)) # background='#f0f0f0' heredado
        style.configure('TEntry', font=('Arial', 11), padding=5)
        # No se configuran estilos de botón personalizados aquí (Green, Red, Plot)
        # Se usará el estilo por defecto 'TButton' de ttk

        ttk.Label(main_frame, text="Función f(x):").grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.entrada_funcion = ttk.Entry(main_frame, width=40)
        self.entrada_funcion.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.entrada_funcion.insert(0, "x**3 * math.log(x)")

        ttk.Label(main_frame, text="Límite inferior (a):").grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.entrada_a = ttk.Entry(main_frame, width=15)
        self.entrada_a.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        self.entrada_a.insert(0, "1")

        ttk.Label(main_frame, text="Límite superior (b):").grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.entrada_b = ttk.Entry(main_frame, width=15)
        self.entrada_b.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        self.entrada_b.insert(0, "3")

        ttk.Label(main_frame, text="Número de subintervalos (N >=1):").grid(row=3, column=0, padx=5, pady=10, sticky="w")
        self.entrada_N = ttk.Entry(main_frame, width=15)
        self.entrada_N.grid(row=3, column=1, padx=5, pady=10, sticky="w")
        self.entrada_N.insert(0, "100")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)

        # Botones usan el estilo ttk.Button por defecto (no se especifica 'style=')
        self.boton_calcular = ttk.Button(button_frame, text="Calcular Integral", command=self.calcular_integral_trapecio)
        self.boton_calcular.pack(side=tk.LEFT, padx=5)

        self.boton_limpiar = ttk.Button(button_frame, text="Limpiar Campos", command=self.limpiar_campos)
        self.boton_limpiar.pack(side=tk.LEFT, padx=5)
        
        self.boton_graficar = ttk.Button(button_frame, text="Graficar Resultado", command=self.graficar_resultado, state=tk.DISABLED)
        self.boton_graficar.pack(side=tk.LEFT, padx=5)

        ttk.Label(main_frame, text="Resultado:").grid(row=5, column=0, padx=5, pady=10, sticky="w")
        self.texto_resultado = scrolledtext.ScrolledText(main_frame, height=15, width=70, wrap=tk.WORD, font=('Courier New', 10))
        self.texto_resultado.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.texto_resultado.configure(state='disabled', background='#ffffff') # Fondo blanco para área de texto
        
        main_frame.columnconfigure(1, weight=1)

    def limpiar_campos(self):
        self.entrada_funcion.delete(0, tk.END)
        self.entrada_a.delete(0, tk.END)
        self.entrada_b.delete(0, tk.END)
        self.entrada_N.delete(0, tk.END)
        self.texto_resultado.configure(state='normal')
        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.configure(state='disabled')
        self.entrada_funcion.insert(0, "x**3 * math.log(x)")
        self.entrada_a.insert(0, "1")
        self.entrada_b.insert(0, "3")
        self.entrada_N.insert(0, "100")
        self.boton_graficar.config(state=tk.DISABLED)
        self.x_puntos_graf = None
        self.y_puntos_graf = None
        self.resultado_calculado = None

    def calcular_integral_trapecio(self):
        func_str = self.entrada_funcion.get()
        a_str = self.entrada_a.get()
        b_str = self.entrada_b.get()
        N_str = self.entrada_N.get()

        self.boton_graficar.config(state=tk.DISABLED)
        self.x_puntos_graf = None
        self.y_puntos_graf = None
        self.resultado_calculado = None

        if not all([func_str, a_str, b_str, N_str]):
            messagebox.showerror("Error de Entrada", "Todos los campos son obligatorios.")
            return

        try:
            a = float(a_str)
            b = float(b_str)
            N = int(N_str)
        except ValueError:
            messagebox.showerror("Error de Entrada", "Los límites 'a', 'b' y el número 'N' deben ser numéricos.")
            return

        try:
            retorno_calculo = trapecio_funcion(func_str, a, b, N)
            
            if not (isinstance(retorno_calculo, tuple) and len(retorno_calculo) == 4):
                messagebox.showerror("Error Interno", 
                                     f"La función de cálculo (Trapecio) no devolvió el formato esperado.\nRecibido: {retorno_calculo}")
                self.texto_resultado.configure(state='normal')
                self.texto_resultado.delete(1.0, tk.END)
                self.texto_resultado.insert(tk.END, "Error: Fallo en la comunicación con el núcleo de cálculo del Trapecio.")
                self.texto_resultado.configure(state='disabled')
                return

            resultado, detalles, x_puntos, y_puntos = retorno_calculo
            
            self.texto_resultado.configure(state='normal')
            self.texto_resultado.delete(1.0, tk.END)
            if resultado is not None:
                self.texto_resultado.insert(tk.END, f"Resultado de la integral: {resultado:.8f}\n\n")
                self.texto_resultado.insert(tk.END, "Detalles del Cálculo:\n")
                self.texto_resultado.insert(tk.END, detalles.replace("\\n", "\n"))
                self.x_puntos_graf = x_puntos
                self.y_puntos_graf = y_puntos
                self.resultado_calculado = resultado
                self.boton_graficar.config(state=tk.NORMAL)
            else:
                self.texto_resultado.insert(tk.END, "Error en el cálculo (Trapecio):\n")
                self.texto_resultado.insert(tk.END, detalles)
            self.texto_resultado.configure(state='disabled')

        except Exception as e:
            messagebox.showerror("Error Inesperado en Cálculo (Trapecio)", 
                                 f"Ocurrió un error al procesar la integral: {type(e).__name__}: {e}")
            self.texto_resultado.configure(state='normal')
            self.texto_resultado.delete(1.0, tk.END)
            self.texto_resultado.insert(tk.END, f"Error inesperado en Trapecio: {e}")
            self.texto_resultado.configure(state='disabled')

    def graficar_resultado(self):
        if self.x_puntos_graf is None or self.y_puntos_graf is None or self.resultado_calculado is None:
            messagebox.showwarning("Datos Insuficientes (Trapecio)", 
                                     "No hay datos suficientes para graficar. Por favor, calcula la integral primero.")
            return

        func_str = self.entrada_funcion.get()
        a_str = self.entrada_a.get()
        b_str = self.entrada_b.get()
        N_str = self.entrada_N.get()

        if not all([func_str, a_str, b_str, N_str]):
            messagebox.showerror("Error de Entrada (Trapecio)", "Faltan datos en los campos para graficar (función, a, b, N).")
            return
        try:
            a = float(a_str)
            b = float(b_str)
            N = int(N_str)
        except ValueError:
            messagebox.showerror("Error de Entrada (Trapecio)", "Los valores de a, b, N para graficar no son numéricos.")
            return

        try:
            plot_function_and_integral(
                func_str=func_str, 
                a=a, 
                b=b, 
                N=N, 
                result=self.resultado_calculado,
                x_points_method=self.x_puntos_graf, 
                y_points_method=self.y_puntos_graf,
                method_name="Trapecio"
            )
        except Exception as e:
            messagebox.showerror("Error al Graficar (Trapecio)", f"Ocurrió un error al generar la gráfica: {e}")

if __name__ == '__main__':
    root_trapecio = tk.Tk()
    app_trapecio = CalculadoraTrapecioUI(root_trapecio)
    root_trapecio.mainloop() 