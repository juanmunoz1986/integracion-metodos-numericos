# Aplicación de Integración Numérica

Esta aplicación proporciona una interfaz gráfica para calcular integrales numéricas utilizando diferentes métodos.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
/          # Raíz del proyecto
├── main.py                         # Punto de entrada principal para la aplicación
├── integracion_numerical_app/      # Paquete principal de la aplicación
│   ├── __init__.py
│   ├── core/                       # Módulos con la lógica de los métodos de integración
│   │   ├── __init__.py
│   │   ├── simpson_function_method.py
│   │   ├── trapeze_function_method.py
│   │   └── simpson_vector_method.py
│   └── ui/                         # Módulos con las interfaces gráficas específicas
│       ├── __init__.py
│       ├── main_menu.py            # Script para lanzar el menú principal GUI
│       ├── gui_simpson_function.py
│       ├── gui_trapeze_function.py
│       └── gui_simpson_vector.py
└── README.md                       # Este archivo
```

## Cómo Ejecutar la Aplicación

1.  Asegúrate de tener Python instalado.
2.  Abre una terminal o línea de comandos.
3.  Navega hasta el directorio raíz del proyecto (el directorio que contiene `main.py` y la carpeta `integracion_numerical_app`).
4.  Ejecuta la aplicación utilizando el siguiente comando:

    ```bash
    python main.py
    ```

Esto abrirá la ventana del menú principal, desde donde podrás seleccionar el método de integración deseado. 