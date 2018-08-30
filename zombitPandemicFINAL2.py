#ZOMBIT_PANDEMIC FINAL VERSION 2

class Memoize:
    def __init__(self,f):
        self.f = f
        self.memo = {}
    def __call__(self,*args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


#The following function definition along with class is a set up for representing and
# manipulating fractions
def gcd(a,b):
    #finds gcd of a and b
    A = max(abs(a),abs(b))
    B = min(abs(a),abs(b))
    if B == 0:
        return A
    while True:
        r = A%B
        if r == 0:
            return B
        q = (A-r)/B
        tmp = r
        A = B
        B = tmp

class Fraction:
    def __init__(self,num,denom):
        self.num = num
        self.denom = denom
    def __str__(self):
        return str(self.num) + "/" + str(self.denom)
    def __mul__(self,val):
        f = Fraction(self.num*val,self.denom)
        return f
    def __rmul__(self,val): 
        f = Fraction(self.num*val,self.denom)
        return f
    def __pow__(self,val):
        f = Fraction(self.num**val, self.denom**val)
        return f
    def __add__(self,val):   
        return self.add(val)
    
    def simplify(self):
        g = gcd(self.num,self.denom)
        self.num = self.num/g
        self.denom = self.denom/g
    
    def add(self,frac):
        f = Fraction(self.num*frac.denom + frac.num*self.denom,self.denom*frac.denom)
        return f

    def multiply(self,frac):
        f = Fraction(self.num*frac.num, self.denom*frac.denom)
        return f

    def subtract(self,frac):
        f = self.add(frac.multiply(Fraction(-1,1)))
        return f
    
    def divide(self,frac):
        f = self.multiply(Fraction(frac.denom,frac.num))
        return f

def factorialIter(n):
    p = 1
    if n > 1:
        p = 1
        for i in range(1,n+1):
            p = p*i
    return p
factorialIter = Memoize(factorialIter)

def nChoosekIter(n,k):
    if k > n:
        return 0
    else:
        return factorialIter(n)/factorialIter(k)/factorialIter(n-k)


gcd = Memoize(gcd)
nChoosekIter = Memoize(nChoosekIter)

def connectedGraphs(N, K):
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

    #A simple graph with N vertices can have a maximum of nChoosekIter(N,2) edges
    # this graph is a complete graph on N vertices.
    # As such there is only one graph like this which is trivially connected
    # (every vertex is connected to every other vertex.
    elif K == nChoosekIter(N,2):
        return 1

    #By the reasoning above, if we have more than nChoosek(N,2) edges on a graph
    # with N vertices, then the graph is no longer simple, i.e. it must contain
    # multiple edges.
    elif K > nChoosekIter(N,2):
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
        allPossibleGraphs = nChoosekIter(nChoosekIter(N,2),K)
        numDisconnected = 0
        for n in range(1,N):
            isolatedComponentSize = nChoosekIter(N-1,n-1)
            chooseN = (N-n)*(N-1-n)//2 #Just to make our calculation tidier
            numDisconnectednVerts = 0

            for k in range(0,K+1):
                placingRemEdges = nChoosekIter(chooseN,K-k)
                numWaysIsoConnected = (connectedGraphs(n,k))
                numDisconnectednVerts = numDisconnectednVerts + placingRemEdges*numWaysIsoConnected
            numDisconnected = numDisconnected + isolatedComponentSize*numDisconnectednVerts
            
    return allPossibleGraphs - numDisconnected 
connectedGraphs = Memoize(connectedGraphs)

def nBitsAtMostkWarrens(n,k):
    #So what is the idea here?
    #This function should determine the number of ways to socialise the rabbits such that
    # all warrens are of size AT MOST k.
    #How?
    # We choose one vertex and then of all the remaining we want to pick i-1 more to go with this vertex.
    # Then we want to work out how many ways we can socialise these i vertices to get a size i warren.
    # After this, we need to multiply by the number of ways to get a warren of size AT MOST k among the
    # remaining rabbits. Finally we need to sum over i from 1 to k, (i.e getting the warren including out chosen
    # vertex to be of size i.
    #
    #That is the main idea. We then use some base cases.
    #We can never have a warren of size 1, as EVERY rabbit nudges EXACTLY one other rabbit.
    #We use the convention of 0 rabbits having only one way to be socialised with each other
    #If we have n rabbits and want AT MOST n+i size warrens, as there are n rabbits, there can only be AT MOST an n size warren
    #So therefore nBitsAtMostkWarrens(n,n+i) = nBitsAtMostkWarrens(n,n)

    #Note that we also use the connectedGraphs function to find how many ways to have a size i warren with i rabbits
    #This function was made in a previous challenge.
    S = 0
    if n == 1:
        S = S + 0
    elif n == 0:
        S = S + 1
    elif k > n:
        S = S + nBitsAtMostkWarrens(n,n)
        
    else:
        for i in range(1,k+1):
            S = S + nChoosekIter(n-1,i-1)*(2*connectedGraphs(i,i) + connectedGraphs(i,i-1)*(i-1))*nBitsAtMostkWarrens(n-i,k)
    return S
 
            

nBitsAtMostkWarrens = Memoize(nBitsAtMostkWarrens)

def nBitskWarrens(n,k):
    #We now use the previous function to find the number of socialisations that absolutely has a warren of size k
    #This works as the number of socialisations that have a warren of size AT MOST k, will include all socialisations
    # that have a warren of size AT MOST k-1
    return nBitsAtMostkWarrens(n,k) - nBitsAtMostkWarrens(n,k-1)

print(nBitskWarrens(5,5))

def probability(n,k):
    #Given n rabbits, we want to find the probability of getting a k warren in n-rabbits
    #This simply finds the number of socialisations that has a warren of size k and then multiplies by the probability
    # of getting a particular socialisation
    return (nBitskWarrens(n,k))*Fraction(1,(n-1)**n)
probability = Memoize(probability)


def answer(n):
    #Finally, we calculate expectation in the usual way, SUM n*p(n) for a random variable with support on the integers.
    S = Fraction(0,1)
    for i in range(2,n+1):
        S = S + i*probability(n,i)
    S.simplify() #We must finally simplify the fraction and then output it
    return str(S)
