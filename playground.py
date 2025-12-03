def factors(n: int):
    result = []
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            result.append(i)
    return result

print(factors(28))
print(factors(12))
print(factors(30))