"""
This program simulates a LFSR (Linear-feedback shift register.)
"""
feedback = [1, 1, 1, 1]
zeros = [0, 0, 0, 0]

def increment(arr):
    arr = arr.copy()
    for i in range(len(arr)-1, -1, -1):
        if arr[i] == 0:
            arr[i] = 1
            return arr
        else:
            arr[i] = 0
    return arr


def xor(a, b):
    return 1 if a != b else 0


def runRound(state):
    state = state.copy()
    bit = state[-1]
    progress = 0
    for i in range(len(feedback)-1, -1, -1):
        if feedback[i] == 1:
            progress = xor(progress, state[i])
    return ([progress] + state[:-1], bit)


def main():
    global zeros
    startPoints = []
    for _ in range(2**len(zeros) - 1):
        zeros = increment(zeros)
        startPoints.append(zeros)

    streams = []
    for initial in startPoints:
        state, bit = runRound(initial)
        stream = [bit]
        while(state != initial):
            state, bit = runRound(state)
            stream.append(bit)
        streams.append(stream)
    
    print("Feedback configuration: {}\n".format(feedback))
    for i in range(len(streams)):
        print("Initial:   {}\nKeystream: {}\n".format(startPoints[i], streams[i]))
    
    outFile = open("out.txt", "w")
    for i in range(len(streams)):
        outFile.write("{}: ".format(startPoints[i]))
        for bit in streams[i]:
            outFile.write("{}".format(bit))
        outFile.write("\n")
    outFile.close()


if __name__ == "__main__":
    main()
