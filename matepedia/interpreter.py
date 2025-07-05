from lark import Lark, Transformer, v_args
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")

context = {
    'simbolo': lambda *args: sp.Symbol('x'),
    'mostrar': lambda x: print(x),
    'derivar': lambda f, x: sp.diff(f, x),
    'derivar_n': lambda f, x, n: sp.diff(f, x, n),
    'integrar': lambda f, x, a=None, b=None: sp.integrate(f, (x, a, b)) if a and b else sp.integrate(f, x),
    'resolver': lambda eq, x: sp.solve(eq, x),
    'limite': lambda expr, x, val: sp.limit(expr, x, val),
    'simplificar': lambda expr: sp.simplify(expr),
    'expandir': lambda expr: sp.expand(expr),
    'factorizar': lambda expr: sp.factor(expr),
    'sustituir': lambda expr, x, val: expr.subs(x, val),
    'graficar': lambda f, x, a, b: graficar_funcion(f, x, a, b),
}

def graficar_funcion(f, x, a, b):
    if isinstance(f, sp.Lambda):
        expr = f.body
        args_for_lambdify = f.args[0] if isinstance(f.args[0], tuple) else (f.args[0],)
    else:
        expr = f
        args_for_lambdify = (x,)

    f_lambdified = sp.lambdify(args_for_lambdify, expr, modules=["numpy"])
    X = np.linspace(a, b, 400)

    try:
        Y = f_lambdified(X)
    except Exception as e:
        print(f"Error al evaluar la función para graficar: {e}")
        Y = np.full_like(X, np.nan)

    plt.plot(X, Y)
    plt.title("Gráfico de función")
    plt.xlabel(str(x))
    plt.grid(True)
    plt.show()

@v_args(inline=True)
class EvalMatepedia(Transformer):
    def __init__(self):
        self.vars = {}

    def assignment(self, name, expr):
        self.vars[name] = expr
        return expr

    def func_def(self, name, args_tree, expr):
        args = [sp.Symbol(str(a)) for a in args_tree.children]
        lambda_func = sp.Lambda(tuple(args), expr)
        self.vars[str(name)] = lambda_func
        return None

    def args_expr(self, *args):
        return list(args)

    def func_call(self, name, *args):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]

        if isinstance(name, sp.Lambda):
            return name(*args)

        f = self.vars.get(str(name)) or context.get(str(name))
        if isinstance(f, sp.Lambda):
            return f(*args)
        elif callable(f):
            return f(*args)
        else:
            raise Exception(f"Función '{name}' no definida o no invocable.")

    def mostrar_stmt(self, val):
        context['mostrar'](val)
        return None

    def cond_stmt(self, cond_expr, *statements):
        return bool(cond_expr)

    def loop_stmt(self, var, start, end):
        return (str(var), int(start), int(end))

    def CNAME(self, name):
        name_str = str(name)
        if name_str in self.vars:
            return self.vars[name_str]
        return sp.Symbol(name_str)

    def NUMBER(self, val):
        return float(val)

    def expr(self, a, *rest_chains):
        res = a
        for op_token_str, val in rest_chains:
            if op_token_str == '+':
                res += val
            elif op_token_str == '-':
                res -= val
        return res

    def add_sub_op_chain(self, op_token, term_result):
        return (str(op_token), term_result)

    def term(self, a, *rest_chains):
        res = a
        for op_token_str, val in rest_chains:
            if op_token_str == '*':
                res *= val
            elif op_token_str == '/':
                res /= val
        return res

    def mul_div_op_chain(self, op_token, power_result):
        return (str(op_token), power_result)

    def pow(self, a, op_token, b):
        return a ** b
    
    def start(self, *statements):
        result = None
        for stmt in statements:
            result = stmt
        return result

def ejecutar_archivo(path):
    transformer = EvalMatepedia()
    with open(path) as f:
        codigo = f.read()
    tree = parser.parse(codigo)
    transformer.transform(tree)

def ejecutar_repl():
    print("Matepedia REPL — escribe 'salir' para terminar")
    repl_transformer = EvalMatepedia()
    while True:
        try:
            linea = input(">>> ")
            if linea.strip().lower() in ["salir", "exit"]:
                break
            if not linea.strip():
                continue

            tree = parser.parse(linea)
            result = repl_transformer.transform(tree)

            if result is not None:
                print(result)

        except Exception as e:
            print(f"Error: {e}")