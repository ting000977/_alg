//使用chatgpt


def sqrt_iterative(n, guess=1.0, tolerance=0.000001):
    x = guess
    count = 0

    while True:
        next_x = (x + n / x) / 2
        count += 1

        print("第", count, "次：", next_x)

        if abs(next_x - x) < tolerance:
            return next_x

        x = next_x


number = 10

answer = sqrt_iterative(number)

print("答案 =", answer)
