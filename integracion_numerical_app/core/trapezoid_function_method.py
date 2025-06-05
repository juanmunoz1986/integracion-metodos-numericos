# Evaluar la función en los puntos xi
x_puntos = [a + i * h for i in range(N + 1)]
y_puntos = []
detalles_calculo += "\nTabla de puntos (x_i, f(x_i)):\n"
detalles_calculo += "-------------------------------------\n"
detalles_calculo += "|   i   |     x_i     |    f(x_i)    |\n"
detalles_calculo += "-------------------------------------\n"

for i in range(N + 1):
    x_i = x_puntos[i]
    try:
        # Reemplazar ^ con ** para la exponenciación si es necesario para eval
        processed_func_str = func_str.replace('^', '**')
        y_i = eval(processed_func_str, {"__builtins__": {}}, {**safe_dict, "x": x_i})
        y_puntos.append(y_i)
        detalles_calculo += f"| {i:^5} | {x_i:^11.6f} | {y_i:^12.6f} |\n"
    except Exception as e:
        error_msg = f"Error al evaluar la función f({x_i}): {e}. Verifica la sintaxis."
        return None, error_msg, None, None # Añadido None para x_puntos, y_puntos
detalles_calculo += "-------------------------------------\n"

detalles_calculo += f"\nResultado de la integral: {integral:.8f}\n"
detalles_calculo += "=====================================\n"

return integral, detalles_calculo, x_puntos, y_puntos 