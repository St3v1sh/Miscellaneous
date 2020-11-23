"""
This program simulates a Trivium cipher.
"""
def xorRec(arr, val):
    if len(arr) == 0:
        return val
    else:
        return xorRec(arr[1:], 1 if val != arr[0] else 0)


def xor(arr):
    if len(arr) > 0:
        return xorRec(arr[1:], arr[0])
    else:
        return 0


def _and(a, b):
    return a == 1 == b


def runRound(shifts):
    a = shifts[0]
    b = shifts[1]
    c = shifts[2]
    outA = xor([a[65], a[92], _and(a[90], a[91])])
    outB = xor([b[68], b[83], _and(b[81], b[82])])
    outC = xor([c[65], c[110], _and(c[108], c[109])])
    bit = xor([outA, outB, outC])
    newA = [xor([a[68], outC])] + a[:-1]
    newB = [xor([b[77], outA])] + b[:-1]
    newC = [xor([c[86], outB])] + c[:-1]
    return (newA, newB, newC, bit)


def main():
    shiftA = [0 for _ in range(93)]
    shiftB = [0 for _ in range(84)]
    shiftC = [(0 if i < 108 else 1) for i in range(111)]

    warmupBits = []
    for _ in range(70):
        shiftA, shiftB, shiftC, bit = runRound([shiftA, shiftB, shiftC])
        warmupBits.append(bit)
    
    print(warmupBits)

    outFile = open("out.txt", "w")
    for bit in warmupBits:
        outFile.write("{}".format(bit))
    outFile.close()


if __name__ == "__main__":
    main()