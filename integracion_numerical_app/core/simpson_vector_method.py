import math

def simpson_un_tercio(x_valores, fx_valores):
    """
    Aproxima la integral de una función tabulada f(x) usando el método de Simpson 1/3.

    Parámetros:
        x_valores (list[float]): Lista de valores de x, deben estar equiespaciados.
        fx_valores (list[float]): Lista de valores de f(x) correspondientes a x_valores.

    Retorna:
        Tupla (float, str, list[float], list[float]):
            - Aproximación numérica de la integral.
            - Cadena con los detalles del cálculo (incluyendo la tabla).
            - Lista de coordenadas x de los puntos de entrada (los mismos que x_valores).
            - Lista de coordenadas y (f(x)) de los puntos de entrada (los mismos que fx_valores).

    Excepciones:
        ValueError si las entradas no son válidas (ej: longitudes no coinciden,
                     número de puntos no es impar, x no equiespaciados, etc.).
    """
    n_puntos = len(x_valores)

    # 1. Validaciones básicas
    if n_puntos != len(fx_valores):
        raise ValueError("Los vectores x_valores y fx_valores deben tener la misma longitud.")

    if n_puntos < 3:
        raise ValueError("Se requieren al menos 3 puntos para el método de Simpson 1/3.")

    if (n_puntos - 1) % 2 != 0: # (n_puntos - 1) es el número de intervalos N, que debe ser par.
                                # Esto implica que n_puntos debe ser impar.
        raise ValueError(f"El número de puntos ({n_puntos}) debe ser impar para Simpson 1/3 "
                         f"(lo que implica un número par de {n_puntos - 1} intervalos).")

    # 2. Verificar que x_valores estén equiespaciados y calcular h
    h = x_valores[1] - x_valores[0]
    if h <= 0:
        raise ValueError("Los valores de x deben estar en orden ascendente y h debe ser positivo.")

    for i in range(1, n_puntos - 1):
        h_actual = x_valores[i+1] - x_valores[i]
        # Usar una tolerancia para comparar floats
        if not math.isclose(h_actual, h, rel_tol=1e-9):
            raise ValueError(f"Los valores de x no están equiespaciados. "
                             f"Se esperaba h={h:.6f} pero se encontró h={h_actual:.6f} "
                             f"entre x_{i}={x_valores[i]} y x_{i+1}={x_valores[i+1]}.")

    # 3. Aplicar la fórmula de Simpson 1/3
    suma_terminos_formula = 0.0
    # Necesitamos los términos individuales para mostrar la suma explícita
    terminos_para_la_suma_expandida = []

    # Primer término: f(x_0)
    coef = 1
    termino_actual = coef * fx_valores[0]
    suma_terminos_formula += termino_actual
    terminos_para_la_suma_expandida.append(f"{termino_actual:.8f}")

    # Términos intermedios
    for i in range(1, n_puntos - 1):
        if i % 2 == 1: coef = 4
        else: coef = 2
        termino_actual = coef * fx_valores[i]
        suma_terminos_formula += termino_actual
        terminos_para_la_suma_expandida.append(f"{termino_actual:.8f}")

    # Último término: f(x_N)
    coef = 1
    termino_actual = coef * fx_valores[n_puntos - 1]
    suma_terminos_formula += termino_actual
    terminos_para_la_suma_expandida.append(f"{termino_actual:.8f}")
    
    integral_aprox = (h / 3.0) * suma_terminos_formula

    # --- Construir la cadena de detalles del cálculo REFINADA ---
    num_intervalos = n_puntos - 1
    detalle_calculo = f"Método de Simpson 1/3 con {n_puntos} puntos ({num_intervalos} intervalos).\\n"
    detalle_calculo += f"Paso h = {h:.8f}\\n\\n"

    detalle_calculo += "Operación de la suma (según la fórmula de Simpson 1/3):\\n"
    detalle_calculo += f"Integral ≈ ({h:.8f}/3) * [ "
    detalle_calculo += " + ".join(terminos_para_la_suma_expandida)
    detalle_calculo += " ]\\n"
    detalle_calculo += f"           ≈ ({h:.8f}/3) * [ {suma_terminos_formula:.8f} ] = {integral_aprox:.8f}\\n"

    return integral_aprox, detalle_calculo, x_valores, fx_valores


def solicitar_vector(nombre_vector):
    """Solicita al usuario una cadena de números y la convierte en una lista de floats."""
    while True:
        entrada_str = input(f"Ingrese los valores para el vector {nombre_vector} separados por comas o espacios (ej: 1, 2.5, 3): ")
        # Reemplazar comas por espacios para un split único
        elementos_str = entrada_str.replace(",", " ").split()
        if not elementos_str:
            print("Entrada vacía. Por favor, ingrese al menos un número.")
            continue
        try:
            vector = [float(elem) for elem in elementos_str]
            return vector
        except ValueError:
            print("Entrada inválida. Asegúrese de que todos los elementos sean números válidos (ej: 1 o 2.3). Intente de nuevo.")

if __name__ == "__main__":
    print("---------------------------------------------------------")
    print("  Calculadora de Integral por Simpson 1/3 (Datos Tabulados)")
    print("---------------------------------------------------------")
    print("Este programa calcula la integral aproximada usando el método de Simpson 1/3")
    print("a partir de datos tabulados (vectores x y f(x)).")
    print("Asegúrese de que:")
    print("  1. Los valores de 'x' estén equiespaciados.")
    print("  2. El número total de puntos de datos sea IMPAR y al menos 3.")
    print("     (Esto significa que el número de subintervalos debe ser PAR y al menos 2).")
    print("---------------------------------------------------------")

    try:
        print("\n--- Ingreso de Datos ---")
        x_usuario = solicitar_vector("x")
        fx_usuario = solicitar_vector("f(x)")

        print("\n--- Procesando... ---")
        resultado, detalles, _, _ = simpson_un_tercio(x_usuario, fx_usuario)
        
        print("\n--- Detalles del Cálculo ---")
        print(detalles)
        print("--- Resultado Final ---")
        print(f"La aproximación de la integral usando Simpson 1/3 es: {resultado:.8f}")

    except ValueError as ve:
        print(f"\nError: {ve}")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}") 