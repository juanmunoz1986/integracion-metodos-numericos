import math

_COMMON_MATH_SCOPE = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "asinh": math.asinh, "acosh": math.acosh, "atanh": math.atanh,
    "exp": math.exp, "log": math.log, "log10": math.log10, "log2": math.log2, "log1p": math.log1p,
    "sqrt": math.sqrt, "pow": math.pow,
    "fabs": math.fabs, "ceil": math.ceil, "floor": math.floor,
    "degrees": math.degrees, "radians": math.radians,
    "pi": math.pi, "e": math.e, "tau": math.tau,
    "abs": abs
}

def trapecio_funcion(f_str, a, b, N):
    """
    Aproxima la integral de f(x) (dada como cadena) en [a, b] usando la regla del Trapecio.

    Parámetros:
        f_str (str): La función como cadena, ej. "x**2 * exp(-x)".
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        N (int): Número de subintervalos (debe ser >= 1).

    Retorna:
        Tupla (float, str, list[float], list[float]):
            - Aproximación numérica de la integral.
            - Cadena con los detalles del cálculo.
            - Lista de coordenadas x de los puntos evaluados.
            - Lista de coordenadas y (f(x)) de los puntos evaluados.
    """
    # 1. Validaciones de entrada
    if not isinstance(f_str, str) or not f_str:
        # raise ValueError("La función 'f_str' debe ser una cadena de texto no vacía.")
        return None, "Error: La función 'f_str' debe ser una cadena de texto no vacía.", None, None
    if b <= a:
        # raise ValueError("El límite superior 'b' debe ser mayor que el límite inferior 'a'.")
        return None, "Error: El límite superior 'b' debe ser mayor que el límite inferior 'a'.", None, None
    if not isinstance(N, int):
        # raise ValueError("El número de subintervalos 'N' debe ser un entero.")
        return None, "Error: El número de subintervalos 'N' debe ser un entero.", None, None
    if N < 1:
        # raise ValueError("El número de subintervalos 'N' debe ser mayor o igual a 1.")
        return None, "Error: El número de subintervalos 'N' debe ser mayor o igual a 1.", None, None

    # Crear función evaluable
    eval_globals = {**_COMMON_MATH_SCOPE, "math": math}
    try:
        func = lambda x_val: eval(f_str, eval_globals, {"x": x_val})
        func(a) # Probar
    except NameError as ne:
        error_msg = (
            f"Error al parsear la función f_str='{f_str}'. Variable o función no reconocida: {ne}. "
            f"Asegúrate de que esté disponible (ej: 'exp', 'sin', 'pi') o usa 'math.nombre_funcion()'."
        )
        # raise ValueError(error_msg)
        return None, error_msg, None, None
    except Exception as e:
        error_msg = f"Error al parsear o evaluar inicialmente f_str='{f_str}' en x={a}: {e}"
        # raise ValueError(error_msg)
        return None, error_msg, None, None

    h = (b - a) / N
    
    puntos_evaluacion = [] # Lista para almacenar (índice_str, x_i, fx_i)

    # f(x_0)
    try:
        fx0 = func(a)
    except Exception as e:
        # raise ValueError(f"Error al evaluar f(x)='{f_str}' en x = {a:.4f}: {e}")
        return None, f"Error al evaluar f(x)='{f_str}' en x = {a:.4f}: {e}", None, None
    puntos_evaluacion.append(("x_0 (a)", a, fx0))

    suma_terminos_intermedios_2fx = 0.0
    
    # Suma de 2*f(x_i) para i=1 hasta N-1
    for i in range(1, N): # De x_1 a x_{N-1}
        x_i = a + i * h
        try:
            fx_i = func(x_i)
        except Exception as e:
            # raise ValueError(f"Error al evaluar f(x)='{f_str}' en x = {x_i:.4f}: {e}")
            return None, f"Error al evaluar f(x)='{f_str}' en x = {x_i:.4f}: {e}", None, None
        puntos_evaluacion.append((f"x_{i}", x_i, fx_i))
        suma_terminos_intermedios_2fx += 2 * fx_i
    
    # f(x_N)
    try:
        fxN = func(b) # x_N es b
    except Exception as e:
        # raise ValueError(f"Error al evaluar f(x)='{f_str}' en x = {b:.4f}: {e}")
        return None, f"Error al evaluar f(x)='{f_str}' en x = {b:.4f}: {e}", None, None
    puntos_evaluacion.append((f"x_{N} (b)", b, fxN))

    integral_aprox = (h / 2.0) * (fx0 + suma_terminos_intermedios_2fx + fxN)
    suma_total_corchetes = fx0 + suma_terminos_intermedios_2fx + fxN

    # --- Construir la cadena de detalles del cálculo ---
    detalle_calculo = f"Método del Trapecio con {N + 1} puntos ({N} intervalos).\\n"
    detalle_calculo += f"Función f(x) = {f_str}\\nLímites [{a}, {b}], N = {N}\\n\\n"
    
    detalle_calculo += "Cálculo de h:\\n"
    detalle_calculo += f"h = ( {b} - {a} ) / {N} = {h:.8f}\\n\\n"
        
    detalle_calculo += "Tabla de evaluación de la función en los puntos:\\n"
    detalle_calculo += "Índice  | x_i          | f(x_i)\\n"
    detalle_calculo += "-------------------------------\\n"
    for idx_str, x_val, fx_val in puntos_evaluacion:
        detalle_calculo += f"{idx_str:<7} | {x_val:<12.8f} | {fx_val:.8f}\\n"
    detalle_calculo += "\\n"

    detalle_calculo += "Suma completa (según la fórmula del Trapecio):\\n"
    detalle_calculo += f"Integral ≈ ({h:.8f}/2) * [ "
    
    sum_parts = []
    sum_parts.append(f"{fx0:.8f}") # f(x0)
    for i in range(1, N):
        # fx_i_val es puntos_evaluacion[i][2]
        sum_parts.append(f"2*{puntos_evaluacion[i][2]:.8f}") 
    sum_parts.append(f"{fxN:.8f}") # f(xN)
    
    detalle_calculo += " + ".join(sum_parts)
    detalle_calculo += " ]\\n"
    
    # Mostrar los valores que se suman dentro del corchete (ya multiplicados por 2 donde corresponde)
    detalle_calculo += f"           ≈ ({h:.8f}/2) * [ {fx0:.8f}"
    if N > 1: # Solo mostrar suma de intermedios si existen
        # Reconstruimos la suma de los 2*f(xi) para mostrarla
        suma_intermedios_display = " + ".join([f"{2*p[2]:.8f}" for p in puntos_evaluacion[1:-1]])
        if suma_intermedios_display:
             detalle_calculo += f" + {suma_intermedios_display}"
    detalle_calculo += f" + {fxN:.8f} ]\\n"

    detalle_calculo += f"           ≈ ({h:.8f}/2) * [ {suma_total_corchetes:.8f} ] = {integral_aprox:.8f}\\n"
    detalle_calculo += "\\n"

    x_puntos = [p[1] for p in puntos_evaluacion]
    y_puntos = [p[2] for p in puntos_evaluacion]

    return integral_aprox, detalle_calculo, x_puntos, y_puntos

if __name__ == '__main__':
    # Ejemplo de uso directo (para pruebas)
    print("--- Prueba del Módulo: Método del Trapecio (Función) ---")
    f_prueba = "x**3 * log(x)"
    a_prueba = 1
    b_prueba = 3
    N_prueba = 10
    print(f"Calculando integral de f(x) = {f_prueba} de {a_prueba} a {b_prueba} con N = {N_prueba}")
    try:
        resultado, detalles, x_coords, y_coords = trapecio_funcion(f_prueba, a_prueba, b_prueba, N_prueba)
        print("\n--- Detalles ---")
        print(detalles.replace("\\n", "\n"))
        print("--- Resultado ---")
        print(f"Integral aproximada: {resultado:.8f}")
        # print(f"Puntos x: {x_coords}") # Descomentar para depurar
        # print(f"Puntos y: {y_coords}") # Descomentar para depurar
    except ValueError as ve:
        # Esto no debería ocurrir si los returns de error funcionan
        print(f"Error de ValueError: {ve}") 
    except TypeError: # Capturar si la función devuelve menos de 4 valores
        print(f"Error: La función trapecio_funcion no devolvió suficientes valores. Probablemente falló antes de generar los puntos.")
        # Aquí se podría imprimir el resultado y detalles si solo esos fueron devueltos.
        # Para este ejemplo, simplemente indicamos el problema.
    except Exception as e:
        print(f"Error inesperado: {e}")

    print("\n--- Prueba con sin(x) ---")
    f_prueba_2 = "sin(x)"
    a_prueba_2 = 0
    b_prueba_2 = math.pi
    N_prueba_2 = 50 
    # Integral de sin(x) de 0 a pi es 2
    print(f"Calculando integral de f(x) = {f_prueba_2} de {a_prueba_2} a {b_prueba_2} con N = {N_prueba_2}")
    try:
        resultado_2, detalles_2, x_c2, y_c2 = trapecio_funcion(f_prueba_2, a_prueba_2, b_prueba_2, N_prueba_2)
        print("\n--- Detalles ---")
        print(detalles_2.replace("\\n", "\n"))
        print("--- Resultado ---")
        print(f"Integral aproximada: {resultado_2:.8f} (Valor esperado: 2.0)")
    except ValueError as ve:
        print(f"Error: {ve}")
    except TypeError:
        print(f"Error: La función trapecio_funcion para sin(x) no devolvió suficientes valores.")
    except Exception as e:
        print(f"Error inesperado: {e}") 