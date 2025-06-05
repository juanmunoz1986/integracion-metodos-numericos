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

def simpson_funcion(f_str, a, b, N):
    """
    Aproxima la integral de f(x) (dada como cadena) en [a, b] usando Simpson 1/3.

    Parámetros:
        f_str (str): La función como cadena, ej. "x**2 * exp(-x)".
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        N (int): Número de subintervalos (debe ser par y >= 6).

    Retorna:
        Tupla (float, str, list[float], list[float]):
            - Aproximación numérica de la integral.
            - Cadena con los detalles del cálculo.
            - Lista de coordenadas x de los puntos evaluados.
            - Lista de coordenadas y (f(x)) de los puntos evaluados.
    """
    # 1. Validaciones de entrada
    if not isinstance(f_str, str) or not f_str:
        return None, "Error: La función 'f_str' debe ser una cadena de texto no vacía.", None, None
    if b <= a:
        return None, "Error: El límite superior 'b' debe ser mayor que el límite inferior 'a'.", None, None
    if not isinstance(N, int):
        return None, "Error: El número de subintervalos 'N' debe ser un entero.", None, None
    if N < 6:
        return None, "Error: El número de subintervalos 'N' debe ser mayor que 4 (es decir, >= 6).", None, None
    if N % 2 != 0:
        return None, "Error: El número de subintervalos 'N' debe ser par.", None, None

    # Crear función evaluable
    eval_globals = {**_COMMON_MATH_SCOPE, "math": math}
    try:
        func = lambda x_val: eval(f_str, eval_globals, {"x": x_val})
        func(a) 
    except NameError as ne:
        error_msg = (
            f"Error al parsear la función f_str='{f_str}'. Variable o función no reconocida: {ne}. "
            f"Asegúrate de que esté disponible (ej: 'exp', 'sin', 'pi') o usa 'math.nombre_funcion()'."
        )
        return None, error_msg, None, None
    except Exception as e:
        error_msg = f"Error al parsear o evaluar inicialmente f_str='{f_str}' en x={a}: {e}"
        return None, error_msg, None, None

    h = (b - a) / N
    
    puntos_evaluacion_simpson = [] # (índice_str, x_i, fx_i, coeficiente, termino_formula)
    suma_terminos_formula = 0.0

    # Calcular f(x_i) y aplicar coeficientes de Simpson
    for i in range(N + 1): # N+1 puntos, de x_0 a x_N
        x_i = a + i * h
        try:
            fx_i = func(x_i)
        except Exception as e:
            return None, f"Error al evaluar f(x)='{f_str}' en x = {x_i:.4f}: {e}", None, None

        coeficiente = 0
        idx_str = f"x_{i}"
        if i == 0:
            coeficiente = 1
            idx_str = "x_0 (a)"
        elif i == N:
            coeficiente = 1
            idx_str = f"x_{N} (b)"
        elif i % 2 == 1: # Impar
            coeficiente = 4
        else: # Par (no extremo)
            coeficiente = 2
        
        termino_actual = coeficiente * fx_i
        suma_terminos_formula += termino_actual
        puntos_evaluacion_simpson.append((idx_str, x_i, fx_i, coeficiente, termino_actual))

    integral_aprox = (h / 3.0) * suma_terminos_formula

    # --- Construir la cadena de detalles del cálculo ---
    detalle_calculo = f"Método de Simpson 1/3 con {N + 1} puntos ({N} intervalos).\\n"
    detalle_calculo += f"Función f(x) = {f_str}\\nLímites [{a}, {b}], N = {N}\\n\\n"

    detalle_calculo += "Cálculo de h:\\n"
    detalle_calculo += f"h = ( {b} - {a} ) / {N} = {h:.8f}\\n\\n"
        
    detalle_calculo += "Tabla de evaluación de la función y términos de Simpson:\\n"
    detalle_calculo += "Índice  | x_i          | f(x_i)       | Coef. | Coef*f(x_i)\\n"
    detalle_calculo += "-----------------------------------------------------------\\n"
    for idx_str, x_val, fx_val, coef, term_val in puntos_evaluacion_simpson:
        detalle_calculo += f"{idx_str:<7} | {x_val:<12.8f} | {fx_val:<12.8f} | {coef:<5} | {term_val:.8f}\\n"
    detalle_calculo += "\\n"

    detalle_calculo += "Suma completa (según la fórmula de Simpson 1/3):\\n"
    detalle_calculo += f"Integral ≈ ({h:.8f}/3) * [ "
    
    # Mostrar la suma de los términos individuales (coef*f(xi))
    sum_parts_display = " + ".join([f"{p[4]:.8f}" for p in puntos_evaluacion_simpson])
    detalle_calculo += sum_parts_display
    detalle_calculo += " ]\\n"
    
    detalle_calculo += f"           ≈ ({h:.8f}/3) * [ {suma_terminos_formula:.8f} ] = {integral_aprox:.8f}\\n"
    detalle_calculo += "\\n" 

    x_puntos = [p[1] for p in puntos_evaluacion_simpson]
    y_puntos = [p[2] for p in puntos_evaluacion_simpson]

    return integral_aprox, detalle_calculo, x_puntos, y_puntos

def solicitar_funcion_str():
    while True:
        f_str = input("Ingrese la función f(x) (ej: x**2 * exp(-x) o sin(x)/x ): ")
        if f_str:
            return f_str
        print("La cadena de la función no puede estar vacía. Intente de nuevo.")

def solicitar_float(mensaje_prompt):
    while True:
        try:
            valor = float(input(mensaje_prompt))
            return valor
        except ValueError:
            print("Entrada inválida. Debe ingresar un número. Intente de nuevo.")

def solicitar_N_simpson():
    while True:
        try:
            N = int(input("Número de subintervalos N (par, >= 6): "))
            if N < 6:
                print("N debe ser mayor que 4 (es decir, >= 6).")
            elif N % 2 != 0:
                print("N debe ser un número par.")
            else:
                return N
        except ValueError:
            print("Entrada inválida. N debe ser un número entero.")

if __name__ == "__main__":
    print("------------------------------------------------------------")
    print("  Calculadora de Integral por Simpson 1/3 (Función dada)")
    print("------------------------------------------------------------")
    print("Funciones comunes (sin, cos, exp, log, sqrt, etc.) y constantes (pi, e) disponibles.")
    print("Use 'math.funcion' para otras funciones del módulo math.")
    print("------------------------------------------------------------")

    try:
        print("\n--- Ingreso de Datos ---")
        funcion_str = solicitar_funcion_str()
        lim_a = solicitar_float("Límite inferior a: ")
        lim_b = solicitar_float("Límite superior b: ")
        num_N = solicitar_N_simpson()

        print("\n--- Procesando... ---")
        retorno_funcion = simpson_funcion(funcion_str, lim_a, lim_b, num_N)
        
        if len(retorno_funcion) == 4:
            resultado, detalles, x_coords, y_coords = retorno_funcion
            print("\n--- Detalles del Cálculo ---")
            print(detalles) 
            print("--- Resultado Final ---")
            print(f"La aproximación de la integral de '{funcion_str}' es: {resultado:.8f}")
            # print(f"Puntos x: {x_coords}") # Descomentar para depurar
            # print(f"Puntos y: {y_coords}") # Descomentar para depurar
        else:
            # Asumimos que solo devolvió (None, mensaje_error, None, None) o similar
            _, mensaje_error, _, _ = retorno_funcion
            print(f"\nError al procesar: {mensaje_error}")

    except ValueError as ve: # Esto podría capturar errores de solicitar_float o solicitar_N_simpson
        print(f"\nError de entrada: {ve}")
    except Exception as e:
        print(f"\nOcurrió un error inesperado general: {e}") 