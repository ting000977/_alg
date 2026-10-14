def sym_diff(expr):
    op = expr[0]

    if op == "const":
        return ("const", 0)

    if op == "var":
        return ("const", 1) if expr[1] == "x" else ("const", 0)

    if op == "add":
        return ("add", sym_diff(expr[1]), sym_diff(expr[2]))

    if op == "mul":
        a, b = expr[1], expr[2]
        return (
            "add",
            ("mul", sym_diff(a), b),
            ("mul", a, sym_diff(b))
        )

    if op == "pow":
        a, n = expr[1], expr[2]
        if n == 0:
            return ("const", 0)
        return (
            "mul",
            ("const", n),
            ("mul", ("pow", a, n - 1), sym_diff(a))
        )

    if op == "sin":
        a = expr[1]
        return ("mul", ("cos", a), sym_diff(a))

    if op == "cos":
        a = expr[1]
        return (
            "mul",
            ("const", -1),
            ("mul", ("sin", a), sym_diff(a))
        )

    raise ValueError(f"不支援的運算子：{op}")


def show(expr):
    op = expr[0]

    if op in ("const", "var"):
        return str(expr[1])

    if op in ("add", "mul"):
        symbol = "+" if op == "add" else "*"
        return f"({show(expr[1])} {symbol} {show(expr[2])})"

    if op == "pow":
        return f"({show(expr[1])}^{expr[2]})"

    if op in ("sin", "cos"):
        return f"{op}({show(expr[1])})"


# f(x) = x^3 + 2x
expr = (
    "add",
    ("pow", ("var", "x"), 3),
    ("mul", ("const", 2), ("var", "x"))
)

result = sym_diff(expr)
print(show(result))
