import typing, random
from timeit import default_timer as timer
from sys import maxsize

"""Maximum subarray problem algorithms implementations in python 3.x"""

def bruteForceTripleLoop(arr: list, *args) -> tuple:
    #O(n^3) time, O(1) space
    max_sum = 0
    n = len(arr)

    for i in range(n):
        for j in range(i,n):
            partial = 0
            for k in range(i,j+1):
                partial += arr[k]

            if (partial > max_sum):
                max_sum = partial
                low = i
                high = j

    return (max_sum, low, high)


def bruteForceDoubleLoop(arr: list, *args) -> tuple:
    #O(n^2) time, O(1) space
    max_sum = 0
    n = len(arr)

    for i in range(n):
        partial = 0
        for j in range(i,n):
            partial += arr[j]
            if (partial > max_sum):
                max_sum = partial
                low = i
                high = j

    return (max_sum, low, high)


def bruteForceHelperArray(arr: list, *args) -> tuple:
    #O(n^2) time, O(n) space
    max_sum = 0
    partial_sums = [0]
    running_sum = 0
    n = len(arr)

    for i in range(n):
        running_sum += arr[i]
        partial_sums.append(running_sum)

    for i in range(n):
        for j in range(i,n):
            partial = partial_sums[j+1] - partial_sums[i]
            if (partial > max_sum):
                max_sum = partial
                low = i
                high = j

    return (max_sum, low, high)


def divideAndConquer(arr: list, low: int, high: int, *args) -> tuple:
    #O(nlogn) time, O(nlogn) space from stack calls
    if low == high - 1:
        return  (arr[low], low, high)
    else:

        mid = (low + high) // 2
        left_max, left_low, left_high,  = divideAndConquer(arr, low, mid)
        right_max, right_low, right_high,  = divideAndConquer(arr, mid, high)
        cross_max, cross_low, cross_high,  = maxCrossingSum(arr, low, mid, high)

        if (left_max > right_max and left_max > cross_max):
            return (left_max, left_low, left_high)
        elif (right_max > left_max and right_max > cross_max):
            return (right_max, right_low, right_high)
        else:
            return (cross_max, cross_low, cross_high)


def maxCrossingSum(arr: list, low: int, mid: int, high: int, *args) -> tuple:

    sl = -9999999
    st = 0
    cross_low = mid
    for i in range(mid, low-1, -1):
        st = st + arr[i]
        if st > sl:
            sl = st
            cross_low = i

    sr = -9999999
    st = 0
    cross_high = mid + 1
    for i in range(mid+1, high+1):
        st = st + arr[i]
        if st > sr:
            sr = st
            cross_high = i

    return (sl + sr, cross_low, cross_high)


def kadanesAlgorithm(arr: list, *args) -> tuple:
    #O(n) time, O(1) space, also known as "Kadanes's Algorithm"
    max_so_far = -maxsize - 1
    max_highing_here = 0
    size = len(arr)
    low = 0
    high = 0
    s = 0

    for i in range(0,size):

        max_highing_here += arr[i]

        if max_so_far < max_highing_here:
            max_so_far = max_highing_here
            low = s
            high = i

        if max_highing_here < 0:
            max_highing_here = 0
            s = i+1

    return (max_so_far, low, high)


def makeArray(size: int, r: int) -> list:
    return [random.randint(-r,r) for _ in range(size)]


def funcTester(inputfunc, testcase, *args) -> None:

    start = timer()
    res = inputfunc(testcase,*args)
    print("Testing function {}".format(inputfunc.__name__))
    print(res)
    end = timer()
    delay = end - start
    print("T - {} \n".format(delay))


def main():

    random.seed(1066593)
    smallList = makeArray(1000,100)
    bigList = makeArray(1000000,100)
    functions = [bruteForceTripleLoop, bruteForceDoubleLoop, bruteForceHelperArray, divideAndConquer, kadanesAlgorithm]
    n = len(smallList)
    m = len(bigList)

    print("List of length 100")
    for i in range(5):
        funcTester(functions[i],smallList,0,n-1)

    print("\n\nList of length 1000000")
    for j in range(2):
        funcTester(functions[j+3],bigList,0,m-1)


if __name__ == "__main__":
    main()
