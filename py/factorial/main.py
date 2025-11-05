import sys
import big_factorial_cpp

def factorial(n: str|int) -> str:

    if isinstance(n,int) is not None:
        return big_factorial_cpp.factorial(str(n)) 
    else:
        return big_factorial_cpp.factorial(n)

if __name__== "__main__": 
    elements = []
    n=sys.argv[1]
    print(f"{n}! = {factorial(n)}")

