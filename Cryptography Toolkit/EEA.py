"""
This program runs the Extended Euclidean Algorithm.
"""
def EEA(r0, r1):
    if r0 <= r1:
        return None
    
    i = 1
    r = [0, r0, r1]
    s = [1, 0]
    t = [0, 1]
    while r[2] != 0:
        i += 1

        r[0], r[1], r[2] = r[1], r[2], r[1]%r[2]
        q = int((r[0]-r[2])/r[1])
        
        s[0], s[1] = s[1], s[0]-q*s[1]
        t[0], t[1] = t[1], t[0]-q*t[1]
    # Set inverses to None if GCD(r0, r1) != 1
    return r[1], (s[0]+r1)%r1 if r[1] == 1 else None, (t[0]+r0)%r0 if r[1] == 1 else None


def main():
    # print(EEA(1033, 25))
    # print(EEA(1034, 25))
    # print(EEA(1035, 25))
    # print(EEA(1036, 25))
    # print(EEA(7111111, 123456))
    print(EEA(999, 101))


if __name__ == "__main__":
    main()
