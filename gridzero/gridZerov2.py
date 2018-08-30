#THIS IS NOT COMPLETE. MOSTLY JUST SET UP

#GRID ZERO
def buttonPush(n,m,j,i):
    #n and m are number of rows and number of columns respectively
    # and i,j is the location of the button push
    X = [[1 if k == i-1 else 0 for k in range(n)] if l != j-1 else [1 for k in range(n)] for l in range(m)]
    return X

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
    def __mul__(self,frac):
        f = Fraction(self.num*frac.num,self.denom*frac.denom)
        f.simplify()
        return f
    def __rmul__(self,frac): 
        f = Fraction(self.num*frac.denom,self.denom*frac.denom)
        f.simplify()
        return f
    def __pow__(self,val):
        f = Fraction(self.num**val, self.denom**val)
        return f
    def __add__(self,val):
        if isinstance(val,int):
            f = self.add(Fraction(val,1))
        else:
            f = self.add(val)
        f.simplify()
        return f
    
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

def addMatrices(A,B):
    C = [[A[i][j] + B[i][j] for i in range(len(A[0]))] for j in range(len(A))]
    return C

def multiplyToGetijFrac(A,B,i,j):
    m = Fraction(0,1)
    for k in range(len(A[0])):
        m = m + A[i][k]*B[k][j]
    return m
     

def multiplyMatricesFrac(A,B):
    C = []
    for i in range(len(A)):
        C.append([])
        for j in range(len(B[0])):
            C[i].append(multiplyToGetijFrac(A,B,i,j))
    return C
            
def multiplyToGetij(A,B,i,j):
    m = 0
    for k in range(len(A[0])):
        m = m + A[i][k]*B[k][j]
    return m

def multiplyMatrices(A,B):
    C = []
    for i in range(len(A)):
        C.append([])
        for j in range(len(B[0])):
            C[i].append(multiplyToGetij(A,B,i,j))
    return C

def addMod2(A,B):
    C = []
    for i in range(len(A)):
        C.append([])
        for j in range(len(A[0])):
            C[i].append((A[i][j] + B[i][j])%2)
    return C
def printArray(A):
    s = ""
    for i in range(len(A)):
        s = s + "["
        for j in range(len(A[i])):
            s = s + str(A[i][j]) + ", "
        s = s + "]" + "\n"
    print(s)
def deepCopy(A):
    B = []
    for i in range(len(A)):
        B.append([])
        for j in range(len(A[i])):
            B[i].append(A[i][j])
    return B

from random import randint
x = buttonPush(5,5,randint(1,5),randint(1,5))
for i in range(7):
    x = addMod2(x,buttonPush(5,5,randint(1,5),randint(1,5)))

printArray(x)
    
