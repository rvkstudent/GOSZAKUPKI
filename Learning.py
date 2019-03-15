def fib(n):
    fibo = []
    fibo.append(0)
    fibo.append(1)
    for i in range(2, n+1, 1):
        #fibo.append((fibo[i-2]%10 + fibo[i-1]%10)%10)
        fibo.append(fibo[i - 2] + fibo[i - 1])

        print ("Fibo({}) = {}".format(i, fibo[i]))
    return fibo[n]

def main():
    n = int(input())
    print(fib(n))


if __name__ == "__main__":
    main()