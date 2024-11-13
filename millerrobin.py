import random

def is_prime(n, k=5):
    # Special cases
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as 2^r * d + 1 with d odd
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Perform the test k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Test numbers
numbers = [
    67280421310721,
    1701411834604692317316873037158841057,
    2**1001 - 1,
    2**2281 - 1,
    2**9941 - 1
]

for number in numbers:
    print(f"{number} is prime: {is_prime(number)}")
