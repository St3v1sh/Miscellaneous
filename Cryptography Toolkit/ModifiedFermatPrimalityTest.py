"""
This program runs a modified Fermat primality test to find the first
five primes less than 10,000,000.
"""
import time
import random

primes = []

def generate_primes(n):
    global primes
    primes = []
    primes.append(2)
    for i in range(3, n):
        for p in primes:
            if p*p > i:
                primes.append(i)
                break
            if i%p == 0:
                break


# Credit to https://www.geeksforgeeks.org/python-program-for-binary-search/
def binary_search(arr, l, r, x):
    if r >= l:
        mid = l + (r - l)//2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, l, mid-1, x)
        return binary_search(arr, mid+1, r, x)
    return -1


def is_prime(p):
    if binary_search(primes, 0, len(primes), p) != -1:
        return True
    return False


# def is_prime(p):
#     # Reject even numbers
#     if not p&1:
#         return False
#     if p == 1:
#         return False
#     d = 3
#     while d*d <= p:
#         if p%d == 0:
#             return False
#         d += 2
#     return True


def gcd(a, b):
    if a == 0:
        return b
    return gcd(b%a, a)


# def square_multiply(base, exp, mod):
#     res = 1
#     exp = "{0:b}".format(exp)
#     for b in exp:
#         res = (res**2)%mod
#         if b == "1":
#             res = (res*base)%mod
#     return res

    # Too slow
    # len = 0
    # tmp = exp
    # while tmp > 0:
    #     len += 1
    #     tmp >>= 1
    # res = 1
    # for i in range(len):
    #     res = (res**2)%mod
    #     if (exp>>(len-i-1))&1:
    #         res = (res*base)%mod
    # return res


# def square_multiply(base, exp, mod):
#     if exp > 0b0:
#         tmp = square_multiply(base, exp>>1, mod)
#         if exp&1:
#             return (tmp*tmp*base)%mod  # Square and multiply
#         return (tmp*tmp)%mod  # Square
#     return 1


def square_multiply(base, exp, mod):
    if exp > 0:
        tmp = square_multiply(base, exp>>1, mod)
        if exp&1:
            return (((tmp*tmp)%mod)*base)%mod  # Square and multiply
        return (tmp*tmp)%mod  # Square
    return 1


def carmichael_test_strong(p):
    if p <= 4:
        return False
    for i in range(2, p):
        if gcd(i, p) == 1:
            if square_multiply(i, p-1, p) != 1:
                return False
    return not is_prime(p)


def carmichael_test(p):
    s = 100  # Number of tries
    if p <= 4:
        return False
    for i in range(2, min(p, s)):
        a = random.randint(2, p-2)
        if gcd(a, p) == 1:
            if square_multiply(a, p-1, p) != 1:
                return False
    return not is_prime(p)


if __name__ == "__main__":
    generate_primes(10000000)
    print("done generating primes up to 10000000")
    cnt = 0
    for i in range(1000000, 1, -1):
        if carmichael_test(i):
            print(i)
            cnt += 1
            if cnt == 5:
                break
    # print("--------")
    # cnt = 0
    # for i in range(10000000, 1, -1):
    #     if carmichael_test(i):
    #         print(i)
    #         cnt += 1
    #         if cnt == 5:
    #             break

    # print(square_multiply(1234567, 2345678, 3333337))

    # alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # for i in range(len(alphabet)):
    #     print(alphabet[i], square_multiply(i+65, 11, 3763))
