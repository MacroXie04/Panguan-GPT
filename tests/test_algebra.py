from sympy import symbols, simplify, sympify
from tools.algebra import simplify_expr


def test_simplify_expr():
    res = simplify_expr("sin(x)^2 + cos(x)^2")
    assert res["status"] == "ok"
    x = symbols("x")
    assert simplify(sympify(res["simplified_str"]) - 1) == 0


