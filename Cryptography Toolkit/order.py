"""
This program finds the order of some v mod n.
"""
def order_of_rec(n, n_ori, m, i=1):
    if n == 1:
        return i
    elif i >= m:
        return None
    else:
        return order_of_rec(n*n_ori%m, n_ori, m, i+1)


def order_of(n, m):
    return order_of_rec(n, n, m, 1)


def main():
    n = 151
    c = 0
    for i in range(1, n):
        v = order_of(i, n)
        if v == n-1:
            c += 1
        print("Order of {}: {}".format(i, v))
    print("Number of prim roots: {}".format(c))


if __name__ == "__main__":
    main()
