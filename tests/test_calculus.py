from sympy import Rational
from tools.calculus import integrate


def test_integrate_definite():
    res = integrate("x**2", "x", ("x", 0, 1))
    assert res["status"] == "ok"
    # SymPy returns Rational(1,3)
    assert res["result_str"] in {"1/3", "0.333333333333333"}


