import matplotlib.pyplot as plt
import numpy as np
import inspect

def plot_function_and_integral(func_str, a, b, N, result, x_points_method=None, y_points_method=None, method_name=""):
    """
    Grafica la función, el área bajo la curva (integral), y opcionalmente la aproximación del método.

    Args:
        func_str (str): La función como una cadena de texto (ej. "sin(x)*x").
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        N (int): Número de subintervalos usados en el método numérico.
        result (float): Resultado de la integral calculada.
        x_points_method (list, optional): Coordenadas x de los puntos usados por el método.
        y_points_method (list, optional): Coordenadas y de los puntos usados por el método.
        method_name (str, optional): Nombre del método numérico para el título.
    """
    # Namespace para evaluar la función de forma segura
    # Permitimos funciones de numpy y la constante 'e'
    safe_dict = {
        "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
        "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
        "asinh": np.arcsinh, "acosh": np.arccosh, "atanh": np.arctanh,
        "exp": np.exp, "log": np.log, "log10": np.log10, "sqrt": np.sqrt,
        "pi": np.pi, "e": np.e,
        "abs": np.abs, "fabs": np.fabs, "floor": np.floor, "ceil": np.ceil,
        "degrees": np.degrees, "radians": np.radians,
        # Funciones especiales podrían necesitar scipy, por ahora mantenemos numpy
    }

    # Intenta crear la función evaluable
    try:
        # Asegurarse de que la expresión usa 'x' como variable
        if 'x' not in func_str:
            # Si 'x' no está, no podemos graficarla como f(x)
            # Podríamos intentar inferir, pero es mejor ser explícito
            # Por ahora, si es una constante, la graficaremos como una línea horizontal
            # Esto es un caso borde, normalmente la función dependerá de x
            if not any(var in func_str for var in safe_dict.keys()): # Si no es una función conocida
                try:
                    const_val = float(eval(func_str, {"__builtins__": {}}, safe_dict))
                    func = lambda x: const_val * np.ones_like(x) # Crear una función que devuelve la constante
                    func_str_display = f"f(x) = {const_val}"
                except:
                    plt.text(0.5, 0.5, f"Error: No se pudo interpretar la función '{func_str}' para graficar.\nAsegúrate de que usa 'x' como variable (ej. 'x**2') o es una constante válida.",
                             ha='center', va='center', fontsize=10, color='red')
                    plt.title(f"Error de Graficación ({method_name})")
                    plt.show()
                    return
            else: # Es una función conocida pero no usa 'x' (ej. sin(pi/2)). Evaluarla.
                 try:
                    const_val = float(eval(func_str, {"__builtins__": {}}, safe_dict))
                    func = lambda x: const_val * np.ones_like(x)
                    func_str_display = f"f(x) = {func_str} ≈ {const_val:.4f}"
                 except Exception as e:
                    plt.text(0.5, 0.5, f"Error al evaluar función constante '{func_str}': {e}",
                             ha='center', va='center', fontsize=10, color='red')
                    plt.title(f"Error de Graficación ({method_name})")
                    plt.show()
                    return

        else:
            # Reemplazar ^ con ** para la exponenciación si es necesario para eval
            processed_func_str = func_str.replace('^', '**')
            func = lambda x: eval(processed_func_str, {"__builtins__": {}}, {**safe_dict, "x": x})
            func_str_display = f"f(x) = {func_str}"

    except Exception as e:
        # Mostrar un mensaje de error en la figura si la función no se puede parsear
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, f"Error al interpretar la función: {func_str}\n{e}\nAsegúrate de usar 'x' como variable y sintaxis de Python/Numpy.",
                 ha='center', va='center', fontsize=10, color='red')
        plt.title(f"Error de Graficación ({method_name})")
        plt.show()
        return

    # Generar puntos para la curva de la función
    # Usar más puntos para una curva suave, independientemente de N
    x_func = np.linspace(a, b, max(200, N * 10)) 
    try:
        y_func = func(x_func)
    except Exception as e:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, f"Error al evaluar la función '{func_str}' en el rango [{a}, {b}]:\n{e}",
                 ha='center', va='center', fontsize=10, color='red')
        plt.title(f"Error de Graficación ({method_name})")
        plt.show()
        return

    plt.figure(figsize=(12, 7))

    # Graficar la función original
    plt.plot(x_func, y_func, 'b-', label=func_str_display, linewidth=2)

    # Sombrear el área bajo la curva (integral)
    plt.fill_between(x_func, y_func, where=(x_func >= a) & (x_func <= b), color='skyblue', alpha=0.5, label=f"Integral ≈ {result:.5f}")

    # Si se proporcionan los puntos del método, graficarlos y la aproximación
    if x_points_method is not None and y_points_method is not None:
        x_m = np.array(x_points_method)
        y_m = np.array(y_points_method)
        
        plt.plot(x_m, y_m, 'ro', label=f"Puntos del método ({method_name})")

        # Graficar la aproximación del método
        if method_name.lower().startswith("trapecio"):
            for i in range(len(x_m) - 1):
                plt.plot([x_m[i], x_m[i+1]], [y_m[i], y_m[i+1]], 'g--', linewidth=1.5)
            # Añadir etiqueta para la línea una sola vez
            if len(x_m)>1 : plt.plot([], [], 'g--', linewidth=1.5, label='Aproximación por Trapecios')


        elif method_name.lower().startswith("simpson 1/3") and len(x_m) >= 3:
            # Para Simpson, graficamos las parábolas
            # Esto es más complejo, por ahora solo graficaremos líneas entre los puntos del método
            # para dar una idea, o podemos optar por no dibujar la aproximación explícita
            # y solo mostrar los puntos.
            # Graficar segmentos de línea entre cada par de puntos usados por Simpson
            # Esto NO es la parábola, sino una simplificación visual
            for i in range(0, len(x_m) - 2, 2): # Iterar sobre los grupos de 3 puntos
                 # Coeficientes de la parábola que pasa por (x0,y0), (x1,y1), (x2,y2)
                x0, x1, x2 = x_m[i], x_m[i+1], x_m[i+2]
                y0, y1, y2 = y_m[i], y_m[i+1], y_m[i+2]

                # Matriz para resolver el sistema de ecuaciones para A, B, C de Ax^2 + Bx + C = y
                # [[x0^2, x0, 1], [x1^2, x1, 1], [x2^2, x2, 1]] [A, B, C]^T = [y0, y1, y2]^T
                # Evitar singularidad si los puntos x son idénticos (aunque no debería pasar con h > 0)
                if not (np.isclose(x0,x1) or np.isclose(x1,x2) or np.isclose(x0,x2)):
                    mat_A = np.array([[x0**2, x0, 1], [x1**2, x1, 1], [x2**2, x2, 1]])
                    vec_b = np.array([y0, y1, y2])
                    try:
                        coeffs = np.linalg.solve(mat_A, vec_b)
                        A, B, C = coeffs[0], coeffs[1], coeffs[2]
                        
                        # Generar puntos para la parábola en el intervalo [x0, x2]
                        x_parabola = np.linspace(x0, x2, 20)
                        y_parabola = A * x_parabola**2 + B * x_parabola + C
                        
                        # Graficar la parábola del segmento de Simpson
                        if i == 0: # Añadir etiqueta solo para la primera parábola
                             plt.plot(x_parabola, y_parabola, 'm-.', linewidth=1.2, label='Aproximación por Parábolas (Simpson)')
                        else:
                             plt.plot(x_parabola, y_parabola, 'm-.', linewidth=1.2)
                    except np.linalg.LinAlgError:
                        # Si no se puede resolver (ej. puntos colineales de forma que no definen una parábola única)
                        # Dibujar líneas rectas como fallback para este segmento
                        plt.plot([x0, x1], [y0, y1], 'm:', linewidth=1)
                        plt.plot([x1, x2], [y1, y2], 'm:', linewidth=1)
                        if i == 0:
                             plt.plot([],[], 'm:', linewidth=1, label='Segmentos (fallback Simpson)')


            # Línea de fallback si no se dibujaron parábolas (ej. N<2 para Simpson)
            if not any(line.get_label() == 'Aproximación por Parábolas (Simpson)' for line in plt.gca().get_lines()):
                 if len(x_m) > 1: # Si hay al menos dos puntos
                    plt.plot(x_m, y_m, 'm:', linewidth=1, label='Segmentos (Simpson)')


    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(f"Gráfica de la Función y Aproximación de la Integral ({method_name})")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.show()


def plot_vector_integral(x_input, y_input, result, x_points_method, y_points_method, method_name="Simpson 1/3 (Vectores)"):
    """
    Grafica los puntos dados, el área bajo la curva interpolada y la aproximación del método.
    Especial para métodos que toman vectores de puntos (x,y).

    Args:
        x_input (list): Coordenadas x de los puntos de entrada.
        y_input (list): Coordenadas y de los puntos de entrada.
        result (float): Resultado de la integral calculada.
        x_points_method (list): Coordenadas x de los puntos usados por el método (usualmente los mismos que x_input).
        y_points_method (list): Coordenadas y de los puntos usados por el método (usualmente los mismos que y_input).
        method_name (str): Nombre del método numérico para el título.
    """
    x_data = np.array(x_input)
    y_data = np.array(y_input)

    plt.figure(figsize=(12, 7))

    # Graficar los puntos de entrada como la "función" base
    plt.plot(x_data, y_data, 'bo-', label="Puntos de entrada f(x_i)", linewidth=2, markersize=5)

    # Sombrear el área bajo la curva interpolada por los puntos de entrada
    # Para la visualización del área, podemos usar la interpolación lineal entre los puntos
    # o, si el método es Simpson, idealmente sería el área bajo las parábolas.
    # Por simplicidad, usaremos fill_between con los puntos dados.
    # Esto es una aproximación visual del área, la integral real es 'result'.
    if len(x_data) > 1:
        # Crear una "curva" uniendo los puntos para fill_between
        # np.interp podría usarse para más puntos si quisiéramos una curva más suave para el sombreado
        x_fill = np.linspace(x_data.min(), x_data.max(), 200)
        y_fill_interp = np.interp(x_fill, x_data, y_data) # Interpolación lineal
        plt.fill_between(x_fill, y_fill_interp, color='skyblue', alpha=0.5, label=f"Área de Integral (aprox.) ≈ {result:.5f}")

    # Puntos del método (generalmente los mismos que los de entrada para este caso)
    if x_points_method is not None and y_points_method is not None:
        x_m = np.array(x_points_method)
        y_m = np.array(y_points_method)
        
        # Ya están graficados como 'bo-' si son los mismos que los de entrada.
        # Si fueran diferentes, los graficaríamos aquí.
        # plt.plot(x_m, y_m, 'ro', label=f"Puntos del método ({method_name})")

        # Graficar la aproximación del método (parábolas para Simpson)
        if method_name.lower().startswith("simpson 1/3") and len(x_m) >= 3:
            for i in range(0, len(x_m) - 2, 2):
                x0, x1, x2 = x_m[i], x_m[i+1], x_m[i+2]
                y0, y1, y2 = y_m[i], y_m[i+1], y_m[i+2]
                
                if not (np.isclose(x0,x1) or np.isclose(x1,x2) or np.isclose(x0,x2)):
                    mat_A = np.array([[x0**2, x0, 1], [x1**2, x1, 1], [x2**2, x2, 1]])
                    vec_b = np.array([y0, y1, y2])
                    try:
                        coeffs = np.linalg.solve(mat_A, vec_b)
                        A, B, C = coeffs[0], coeffs[1], coeffs[2]
                        x_parabola = np.linspace(x0, x2, 20)
                        y_parabola = A * x_parabola**2 + B * x_parabola + C
                        if i == 0:
                             plt.plot(x_parabola, y_parabola, 'm-.', linewidth=1.2, label='Aproximación por Parábolas (Simpson)')
                        else:
                             plt.plot(x_parabola, y_parabola, 'm-.', linewidth=1.2)
                    except np.linalg.LinAlgError:
                        plt.plot([x0, x1], [y0, y1], 'm:', linewidth=1)
                        plt.plot([x1, x2], [y1, y2], 'm:', linewidth=1)
                        if i == 0:
                             plt.plot([],[], 'm:', linewidth=1, label='Segmentos (fallback Simpson)')
            
            if not any(line.get_label() == 'Aproximación por Parábolas (Simpson)' for line in plt.gca().get_lines()):
                 if len(x_m) > 1:
                    plt.plot(x_m, y_m, 'm:', linewidth=1, label='Segmentos (Simpson)')


    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Gráfica de Puntos y Aproximación de la Integral ({method_name})")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.show() 