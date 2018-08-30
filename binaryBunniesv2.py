#BINARY BUNNIES NUMBER 2

class Memoize:
    def __init__(self,f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not (args in self.memo):
            self.memo[args] = self.f(*args)
        return self.memo[args]

def factorial(n):
    if n <= 1:
        return 1
    else:
        return n*factorial(n-1)

factorial = Memoize(factorial)

def nChooser(n,r):
    if r > n or r <= 0 or r != int(r):
        return 1
    #By using the convention of an undefined n choose r as 1, we will avoid
    # calculation errors when multiplying 2 possible n choose r's
    else:
        return factorial(n)/factorial(r)/factorial(n-r)

def splitTree(seq):
    #This function will take a representation of a binary tree.
    #
    #Considering the first entrant as the root of the tree it will produce 2 new binary trees;
    # these trees are the tree corresponding to the right hand side in our problem, and the tree
    # corresponding to the left hand side of the tree
    #
    #The function will output the result as a size 2 array of arrays. One array will possibly be empty,
    # or in the worst case scenario that the sequence is size 1, we will out put 2 empty arrays.

    lowerTree = []
    upperTree = []

    root = seq[0]# hello */
    
    for i in range(1,len(seq)):
        #We don't need to worry about equality due to the constraints of the problem
        if seq[i] > root:
            upperTree.append(seq[i])
        elif seq[i] < root:
            lowerTree.append(seq[i])

    bothTrees = [lowerTree, upperTree]
    return bothTrees

def answerPre(seq):
    #We will perform a recursive function to do this
    #
    #How does this recursive function work?
    #First of all, if we are given an empty tree then we will just return 1
    #If however, the tree is not empty, then we will multiply together the number of ways to get
    # the tree on the right of the root by the number of ways to get the tree on the left of the root
    # then, we need to also multiply by the number of ways to order the elements great (or lesser) than the
    # root among the open spaces. We do this because if lower numbers appear in between greater numbers,
    # it has no affect on the separate trees.
    
    S = seq
    if len(S) == 0:
        return 1
    bothTrees = splitTree(S)
    return answerPre(bothTrees[0])*answerPre(bothTrees[1])*nChooser(len(S)-1,len(bothTrees[0]))

def answer(seq):
    return str(answerPre(seq))

T = [1,2,3,4,5,6,7,8,9,15,14,23,11]
T = [9,8,7,6,5,4,3,2,1]
print(answerPre2(T,1))
print(answerPre(T))
