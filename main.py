import random
from random import randint


def miller_rabin(n, k):
    if n == 2 or n == 3:
        return True
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


print('Enter number of iterations')
k = int(input())
check = False
while not check:
    # generation random odd number
    test = random.randint(1 << 511, (1 << 512) - 1)
    while test % 2 != 1:
        test = random.randint(1 << 511, (1 << 512) - 1)
    print(test)
    res = miller_rabin(test, k)
    if res:
        print('The number is composite with probability = ' + str((1 / 4) ** k))
        check = True
    else:
        print('The number is composite')
        i = 0
