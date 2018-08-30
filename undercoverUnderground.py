#UNDERCOVER-UNDERGROUND

class Memoize:
    def __init__(self,f):
        self.f = f
        self.memo = {}
    def __call__(self,*args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]
        

def factorial(n):
    if n <= 1:
        return 1
    p = 1
    for i in range(1,n+1):
        p = p*i
    return p

factorial = Memoize(factorial)

def nChoosek(n,k):
    if k > n:
        return 0
    return factorial(n)/factorial(k)/factorial(n-k)
nChoosek = Memoize(nChoosek)

def answer(N, K):
    # your code here
    SUM = 0

    #Let's explain a few of the cases here.
    #A minimum connected graph is a tree and this is equivalent to a graph
    # on N vertices having N-1 edges and being connected
    if K < N-1:
        return 0

    #A graph with 1 vertex and no edges is the only possible graph on
    # one vertex and is trivially connected
    if K == 0 and N == 1:
        return 1

    #A graph with N vertices and N-1 edges is a tree as mentioned above,
    # using Cayley's formula, the number of trees on N vertices is N**(N-2)
    elif K == N-1:
        return N**(N-2)

    #A simple graph with N vertices can have a maximum of nChoosek(N,2) edges
    # this graph is a complete graph on N vertices.
    # As such there is only one graph like this which is trivially connected
    # (every vertex is connected to every other vertex.
    elif K == nChoosek(N,2):
        return 1

    #By the reasoning above, if we have more than nChoosek(N,2) edges on a graph
    # with N vertices, then the graph is no longer simple, i.e. it must contain
    # multiple edges.
    elif K > nChoosek(N,2):
        return 0
    
    #Therefore, the only other situation we need to consider is the one
    # with N vertices and >N-1 edges.
    #
    #We will solve this problem with a recursive formula and then memoizing the
    # results.
    #Instead of directly calculating all of the connected graphs on (N,K),
    # we will take away all of the simple disconnected graphs on N vertices
    # with K edges away from all possible graphs.
    #
    #The number of possible graphs on N vertices with K edges is
    #   nChoosek(nChoosek(N,2),K), i.e. we are choosing K edges from all
    # all possible edges
    #
    #So how can we calculate the number of disconnected graphs?
    #
    #1. Isolate a single vertex. (So we can have at least one vertex not connected)
    #2. Choose n vertices from the remaining vertices
    #3. Find how many ways to connect these n vertices with k edges
    #4. now multiply this by how many ways to place the remaining
    #5. K-k edges between the remaining N-n vertices (so as to not connect
    #  our connected component and the other component).
    #
    #In step 3 we are doing the recursive call of answer(n,k)
    elif K > N-1:
        allPossibleGraphs = nChoosek(nChoosek(N,2),K)
        numDisconnected = 0
        for n in range(1,N):
            isolatedComponentSize = nChoosek(N-1,n-1)
            chooseN = (N-n)*(N-1-n)//2 #Just to make our calculation tidier
            numDisconnectednVerts = 0

            for k in range(0,K+1):
                placingRemEdges = nChoosek(chooseN,K-k)
                numWaysIsoConnected = (answer(n,k))
                numDisconnectednVerts = numDisconnectednVerts + placingRemEdges*numWaysIsoConnected
            numDisconnected = numDisconnected + isolatedComponentSize*numDisconnectednVerts
            
    return allPossibleGraphs - numDisconnected 
answer = Memoize(answer)



