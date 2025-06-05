import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ..core.simpson_vector_method import simpson_un_tercio # Ajustada la importación
from .graph_utility import plot_vector_integral # Importar utilidad de graficación

class CalculadoraSimpsonVectoresUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Integrales - Simpson 1/3 (Vectores)")
        self.root.geometry("650x700") # Un poco más alto para los campos de vectores
        self.root.configure(bg='#f0f0f0')

        # Variables para almacenar los datos para graficar
        self.x_vector_graf = None
        self.y_vector_graf = None
        self.resultado_calculado_graf = None

        main_frame = ttk.Frame(root, padding="20", style='Main.TFrame')
        main_frame.pack(expand=True, fill=tk.BOTH)

        style = ttk.Style()
        style.configure('Main.TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 11))
        style.configure('TEntry', font=('Arial', 11), padding=5)
        style.configure('TButton', font=('Arial', 11, 'bold'), padding=10)
        style.configure('Red.TButton', foreground='white', background='red')
        style.configure('Green.TButton', foreground='white', background='green')
        style.configure('Plot.TButton', foreground='white', background='blue')

        ttk.Label(main_frame, text="Vector X (valores separados por comas o espacios):").grid(row=0, column=0, columnspan=2, padx=5, pady=(10,0), sticky="w")
        self.entrada_vector_x = ttk.Entry(main_frame, width=60)
        self.entrada_vector_x.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,10), sticky="ew")
        self.entrada_vector_x.insert(0, "0, 0.5, 1.0, 1.5, 2.0") # Ejemplo

        ttk.Label(main_frame, text="Vector Y (f(x), valores separados por comas o espacios):").grid(row=2, column=0, columnspan=2, padx=5, pady=(10,0), sticky="w")
        self.entrada_vector_y = ttk.Entry(main_frame, width=60)
        self.entrada_vector_y.grid(row=3, column=0, columnspan=2, padx=5, pady=(0,10), sticky="ew")
        self.entrada_vector_y.insert(0, "0, 0.25, 1.0, 2.25, 4.0") # Ejemplo para y = x^2

        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)

        self.boton_calcular = ttk.Button(button_frame, text="Calcular Integral", command=self.calcular_integral_vectores, style='Green.TButton')
        self.boton_calcular.pack(side=tk.LEFT, padx=5)

        self.boton_limpiar = ttk.Button(button_frame, text="Limpiar Campos", command=self.limpiar_campos, style='Red.TButton')
        self.boton_limpiar.pack(side=tk.LEFT, padx=5)
        
        self.boton_graficar = ttk.Button(button_frame, text="Graficar Resultado", command=self.graficar_resultado_vectores, style='Plot.TButton', state=tk.DISABLED)
        self.boton_graficar.pack(side=tk.LEFT, padx=5)

        ttk.Label(main_frame, text="Resultado:", style='TLabel').grid(row=5, column=0, padx=5, pady=10, sticky="w")
        self.texto_resultado = scrolledtext.ScrolledText(main_frame, height=15, width=70, wrap=tk.WORD, font=('Courier New', 10))
        self.texto_resultado.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.texto_resultado.configure(state='disabled')
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def limpiar_campos(self):
        self.entrada_vector_x.delete(0, tk.END)
        self.entrada_vector_y.delete(0, tk.END)
        self.texto_resultado.configure(state='normal')
        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.configure(state='disabled')
        self.entrada_vector_x.insert(0, "0, 0.5, 1.0, 1.5, 2.0")
        self.entrada_vector_y.insert(0, "0, 0.25, 1.0, 2.25, 4.0")
        self.boton_graficar.config(state=tk.DISABLED)
        self.x_vector_graf = None
        self.y_vector_graf = None
        self.resultado_calculado_graf = None

    def _parse_vector(self, vector_str, vector_name):
        """Convierte una cadena de texto en una lista de floats."""
        try:
            elementos = vector_str.replace(",", " ").split()
            if not elementos:
                raise ValueError(f"El vector {vector_name} no puede estar vacío.")
            return [float(elem) for elem in elementos]
        except ValueError as e:
            # Si es un error de float(elem), el mensaje original es bueno
            # Si es nuestro error de vector vacío, lo usamos
            if f"El vector {vector_name}" in str(e):
                raise
            raise ValueError(f"Error al convertir el vector {vector_name} a números. Verifique el formato: {e}")

    def calcular_integral_vectores(self):
        x_str = self.entrada_vector_x.get()
        y_str = self.entrada_vector_y.get()

        if not x_str or not y_str:
            messagebox.showerror("Error de Entrada", "Ambos vectores X e Y son obligatorios.")
            self.boton_graficar.config(state=tk.DISABLED)
            return

        try:
            x_vector = self._parse_vector(x_str, "X")
            y_vector = self._parse_vector(y_str, "Y")
            
            retorno_calculo = simpson_un_tercio(x_vector, y_vector)

            # Añadir verificación del formato de retorno antes de desempaquetar
            if not (isinstance(retorno_calculo, tuple) and len(retorno_calculo) == 4):
                messagebox.showerror("Error Interno",
                                     f"La función de cálculo de Simpson (vectores) no devolvió el formato esperado.\nRecibido: {retorno_calculo}")
                self.boton_graficar.config(state=tk.DISABLED)
                self.texto_resultado.configure(state='normal')
                self.texto_resultado.delete(1.0, tk.END)
                self.texto_resultado.insert(tk.END, "Error: Fallo en la comunicación con el núcleo de cálculo.")
                self.texto_resultado.configure(state='disabled')
                self.x_vector_graf = None
                self.y_vector_graf = None
                self.resultado_calculado_graf = None
                return

            # Si simpson_un_tercio tuvo éxito, devuelve 4 valores.
            # Si levantó ValueError, se captura abajo.
            resultado, detalles, x_devueltos, y_devueltos = retorno_calculo 
            # x_devueltos e y_devueltos son los mismos que x_vector e y_vector, así que podemos usar los originales.

            self.texto_resultado.configure(state='normal')
            self.texto_resultado.delete(1.0, tk.END)
            self.texto_resultado.insert(tk.END, f"Resultado de la integral: {resultado:.8f}\n\n")
            self.texto_resultado.insert(tk.END, "Detalles del Cálculo:\n")
            self.texto_resultado.insert(tk.END, detalles.replace("\\n", "\n"))
            self.texto_resultado.configure(state='disabled')

            # Guardar datos para graficar
            self.x_vector_graf = x_vector
            self.y_vector_graf = y_vector
            self.resultado_calculado_graf = resultado
            self.boton_graficar.config(state=tk.NORMAL) # Habilitar botón

        except ValueError as ve:
            messagebox.showerror("Error de Entrada o Cálculo", str(ve))
            self.texto_resultado.configure(state='normal')
            self.texto_resultado.delete(1.0, tk.END)
            self.texto_resultado.insert(tk.END, f"Error: {str(ve)}")
            self.texto_resultado.configure(state='disabled')
            self.boton_graficar.config(state=tk.DISABLED) # Deshabilitar botón
            self.x_vector_graf = None
            self.y_vector_graf = None
            self.resultado_calculado_graf = None
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error inesperado: {e}")
            self.boton_graficar.config(state=tk.DISABLED)
            self.x_vector_graf = None
            self.y_vector_graf = None
            self.resultado_calculado_graf = None

    def graficar_resultado_vectores(self):
        if self.x_vector_graf is None or self.y_vector_graf is None or self.resultado_calculado_graf is None:
            messagebox.showwarning("Datos Insuficientes", 
                                     "No hay datos suficientes para graficar. Por favor, calcula la integral primero.")
            return
        
        # Los vectores ya están parseados y almacenados en self.x_vector_graf y self.y_vector_graf
        try:
            plot_vector_integral(
                x_input=self.x_vector_graf,
                y_input=self.y_vector_graf,
                result=self.resultado_calculado_graf,
                x_points_method=self.x_vector_graf, # Para Simpson con vectores, los puntos del método son los de entrada
                y_points_method=self.y_vector_graf,
                method_name="Simpson 1/3 (Vectores)"
            )
        except Exception as e:
            messagebox.showerror("Error al Graficar", f"Ocurrió un error al generar la gráfica: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    app = CalculadoraSimpsonVectoresUI(root)
    root.mainloop() 