# Logo3D

El llenguatge de programació Logo3D modernitza el LOGO clàssic adoptant una nova i elegant sintàxi i situant la popular tortuga en un entorn 3D.

## Usage

```python
import logo3d

# Ejecuta tu programa en logo3d
logo3d.main("Nombre del programa", "Nombre de la funcion a ejecutar", ["Lista de parametros de la funcion"]) 
```

## Contributing
Añadele lo que quieras amigo pero en tu repo.

La gramatica del lenguaje esta en logo3d.g y se ejecuta en antlr4.

En logo3d.py esta el main principal para la ejecucion del programa entero.

En visitor.py esta el visitador del arbol generado por tu programa.

En turtle3d.py esta el modulo encargado de la ventana grafica.
