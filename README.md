# Matepedia

Matepedia es un lenguaje simbólico inspirado en Python diseñado para resolver problemas matemáticos simbólicos y educativos.

## Características

- Declaración y evaluación de funciones matemáticas
- Derivación, integración, simplificación y resolución de ecuaciones
- Condicionales (`si`, `sino`, `fin`) y bucles (`para ... en ... hacer`)
- Soporte para funciones de múltiples variables
- Representación gráfica (`graficar`)
- REPL interactivo

## Ejecución

```bash
pip install -r requirements.txt
python matepedia/main.py ejemplos/basico.mate
```

Para el modo interactivo:

```bash
python matepedia/main.py
```

## Ejemplo

```matepedia
x = simbolo()
funcion f(x) = x^2
area = integrar(f, x, 0, 2)
mostrar(area)
```
