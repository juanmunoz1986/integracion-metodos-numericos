# main.py - Punto de entrada principal para la Aplicación de Integración Numérica

import sys
import os

# Añadir el directorio del proyecto al PYTHONPATH para asegurar que el paquete sea encontrable
# Esto es útil si ejecutas `python main.py` desde la raíz del proyecto.
# Si la raíz del proyecto ya está en PYTHONPATH (ej. si se instala como paquete o se usa un IDE que lo haga),
# esta línea podría no ser estrictamente necesaria, pero no hace daño.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# from integracion_numerical_app.main_menu import start_main_menu_ui
from integracion_numerical_app.ui.main_menu import start_main_menu_ui

if __name__ == "__main__":
    """Inicia la aplicación de integración numérica."""
    print("Iniciando la Aplicación de Integración Numérica...")
    start_main_menu_ui() 