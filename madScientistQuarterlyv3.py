#MAD SCIENTIST QUARTERLY V3

def answer(L,k):
    length = len(L)
    max_current = max_global = L[0]
    summed = 0
    for i in range(1,length):
        singularElement = L[i]
        combinedElements = max_current + singularElement
        max_current = max(singularElement, combinedElements)
        if max_global < max_current and summed <= k-1 and max_current == combinedElements:
            max_global = max_current
            summed = summed+1

    return max_global
L = [40, 91, -68, -36, 24, -67, -32, -23, -33, -52]
k = 7

print(answer(L,k))
