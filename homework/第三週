用chatgpt做的



import itertools
import re


def evaluate(formula, assignment):
    """
    根據 assignment 計算 Boolean formula 的結果。

    例如：
        formula = "(x | y) & (~x | z)"
        assignment = {"x": True, "y": False, "z": True}
    """

    # 把變數名稱替換成 True / False
    expression = formula

    # 先按照變數名稱長度排序，避免變數名稱互相包含
    variables = sorted(assignment.keys(), key=len, reverse=True)

    for var in variables:
        expression = re.sub(
            rf'\b{re.escape(var)}\b',
            str(assignment[var]),
            expression
        )

    # Python 的 ~ 對 bool 並不是我們想要的 NOT
    # 所以把 ~x 改成 not x
    expression = re.sub(r'~\s*(True|False)', r'not \1', expression)

    # Boolean operator
    expression = expression.replace('&', ' and ')
    expression = expression.replace('|', ' or ')

    return eval(expression)


def solve_sat(formula):
    """
    使用暴力法列舉所有真值組合。
    """

    # 找出所有變數
    variables = sorted(set(
        re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', formula)
    ))

    # 排除 Python 關鍵字
    variables = [
        v for v in variables
        if v not in {'True', 'False', 'and', 'or', 'not'}
    ]

    print("Formula:")
    print(" ", formula)
    print()

    print("Variables:")
    print(" ", variables)
    print()

    # 印出真值表標題
    print("Truth Table")
    print("-" * (len(variables) * 8 + 10))

    print(" | ".join(variables) + " | Result")
    print("-" * (len(variables) * 8 + 10))

    solutions = []

    # itertools.product(False, True, repeat=n)
    # 會系統性產生所有 2^n 種組合
    for values in itertools.product([False, True], repeat=len(variables)):

        assignment = dict(zip(variables, values))

        result = evaluate(formula, assignment)

        # 印出這一列
        values_text = " | ".join(
            "T" if assignment[v] else "F"
            for v in variables
        )

        print(f"{values_text} | {'T' if result else 'F'}")

        # 如果公式為 True，就是一組 satisfying assignment
        if result:
            solutions.append(assignment)

    print()
    print("=" * 40)

    if solutions:
        print("SAT")
        print(f"找到 {len(solutions)} 組 satisfying assignments：")
        print()

        for i, solution in enumerate(solutions, 1):
            print(f"{i}: {solution}")

    else:
        print("UNSAT")
        print("不存在任何 satisfying assignment。")

    return solutions


# =====================================
# 測試
# =====================================

formula = "(x | y) & (~x | z)"

solve_sat(formula)
