from matepedia.interpreter import ejecutar_archivo, ejecutar_repl
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ejecutar_archivo(sys.argv[1])
    else:
        ejecutar_repl()
