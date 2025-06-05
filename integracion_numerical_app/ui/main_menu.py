import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

def lanzar_gui_simpson_funcion():
    """Lanza la GUI de la calculadora de Simpson (función) y cierra el menú."""
    print("Lanzando la calculadora de Simpson 1/3 (Función f(x))...")
    try:
        subprocess.Popen([sys.executable, "-m", "integracion_numerical_app.ui.gui_simpson_function"])
        # La ventana del menú se destruirá si la llamada a Popen tiene éxito y root está disponible.
        if 'root' in globals() and root.winfo_exists():
            root.destroy()
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error al lanzar la calculadora Simpson (Función f(x)): {e}")

def lanzar_gui_trapecio_funcion():
    """Lanza la GUI de la calculadora del Trapecio (función) y cierra el menú."""
    print("Lanzando la calculadora del Trapecio (Función f(x))...")
    try:
        subprocess.Popen([sys.executable, "-m", "integracion_numerical_app.ui.gui_trapezoid_function"])
        if 'root' in globals() and root.winfo_exists():
            root.destroy()
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error al lanzar la calculadora Trapecio (Función f(x)): {e}")

def lanzar_gui_simpson_vectores():
    """Lanza la GUI de la calculadora de Simpson (vectores) y cierra el menú."""
    print("Lanzando la calculadora de Simpson 1/3 (Vectores x,y)...")
    try:
        subprocess.Popen([sys.executable, "-m", "integracion_numerical_app.ui.gui_simpson_vectors"])
        if 'root' in globals() and root.winfo_exists():
            root.destroy()
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error al lanzar la calculadora Simpson (Vectores x,y): {e}")



# Variable global para la ventana raíz del menú, para poder cerrarla desde las funciones de lanzamiento.
root = None 

def start_main_menu_ui():
    """Crea y muestra la interfaz gráfica del menú principal."""
    global root # Para poder asignar a la variable global root

    root = tk.Tk()
    root.title("Menú Principal - Integración Numérica")
    root.geometry("480x400") 
    root.resizable(False, False)

    # Estilo
    style = ttk.Style(root)
    style.theme_use('clam')

    # Frame principal
    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.pack(expand=True, fill=tk.BOTH)

    # --- Título del Menú ---
    label_titulo_menu = ttk.Label(main_frame, text="Seleccione un Método de Integración", font=("Arial", 16, "bold"))
    label_titulo_menu.pack(pady=(0, 25))

    # --- Botones de Opción ---
    style.configure("Menu.TButton", font=("Arial", 12), padding=10)

    boton_simpson_funcion = ttk.Button(main_frame, text="Simpson 1/3 (Función f(x))", command=lanzar_gui_simpson_funcion, style="Menu.TButton")
    boton_simpson_funcion.pack(fill=tk.X, pady=5)

    boton_trapecio_funcion = ttk.Button(main_frame, text="Trapecio (Función f(x))", command=lanzar_gui_trapecio_funcion, style="Menu.TButton")
    boton_trapecio_funcion.pack(fill=tk.X, pady=5)

    boton_simpson_vectores = ttk.Button(main_frame, text="Simpson 1/3 (Vectores x,y)", command=lanzar_gui_simpson_vectores, style="Menu.TButton")
    boton_simpson_vectores.pack(fill=tk.X, pady=5)

   

    # Usar lambda para asegurar que root.destroy() se llama correctamente al salir
    boton_salir = ttk.Button(main_frame, text="Salir", command=lambda: root.destroy() if root else None, style="Menu.TButton")
    boton_salir.pack(fill=tk.X, pady=(15, 5))

    root.mainloop()


# --- Iniciar el bucle principal de la GUI del Menú ---
if __name__ == "__main__":
    # Para ejecutar este menú directamente desde la raíz del proyecto:
    # python -m integracion_numerical_app.ui.main_menu 
    # (suponiendo que __main__.py está en la carpeta ui)
    start_main_menu_ui() 