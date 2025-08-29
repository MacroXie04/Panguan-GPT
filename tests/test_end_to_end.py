from sympy import E, symbols, simplify, limit, oo

from orchestrations.pipeline import build_root_agent


def test_end_to_end_basic():
    root = build_root_agent()

    # 1) integral
    s1 = root.run("Compute ∫_0^1 x^2 dx")
    fw1 = s1.get("final_writeup", "")
    assert fw1
    ans1 = s1["solver_output"]["final_answer"]
    assert simplify(ans1) - simplify("1/3") == 0

    # 2) quadratic solve
    s2 = root.run("Solve x^2 - 5x + 6 = 0")
    fw2 = s2.get("final_writeup", "")
    assert fw2
    ans2 = s2["solver_output"]["final_answer"]
    assert "2" in ans2 and "3" in ans2

    # 3) limit test
    s3 = root.run("limit((1+1/n)**n, n, oo)")
    fw3 = s3.get("final_writeup", "")
    assert fw3
    ans3 = s3["solver_output"]["final_answer"]
    # numeric check ~ e
    assert abs(float(E) - float(simplify(ans3))) < 1e-3

    # verification state present and passed
    rep = s3.get("verification_report", {})
    assert rep
    assert rep.get("status") == "passed"


