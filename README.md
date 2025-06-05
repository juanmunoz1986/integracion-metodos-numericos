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

## Cómo Ejecutar la Interfaz Web (Gradio) (Rama: web)

Esta sección aplica si estás en la rama `web` del repositorio, la cual incluye una interfaz de usuario web alternativa construida con Gradio.

1.  **Asegúrate de estar en la rama `web`**.

2.  **Instala o actualiza las dependencias**: Si es la primera vez que usas esta rama o si las dependencias han cambiado, instala los requisitos desde la terminal en el directorio raíz del proyecto:
    ```bash
    pip install -r requirements.txt
    ```
    Esto asegurará que tengas `gradio`, `matplotlib`, y `numpy` instalados.

3.  **Ejecuta la aplicación Gradio**: Desde el directorio raíz del proyecto, ejecuta el siguiente comando en tu terminal:
    ```bash
    python gradio_app.py
    ```

4.  **Abre la interfaz en tu navegador**: Después de ejecutar el comando, verás un mensaje en la terminal similar a:
    ```
    Running on local URL:  http://127.0.0.1:7860
    ```
    (El número de puerto puede variar).
    Abre esta URL en tu navegador web para interactuar con la calculadora de integrales.
    Si ejecutas con `iface.launch(share=True)` en `gradio_app.py`, también obtendrás un enlace público temporal para compartir. 