


def gcd(a, b):

    print ()
    if a == 0 or b == 0:
        return a + b
    return gcd(b, a % b)

def gcd2(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    while True:
        print("a= {}, b = {}".format(a, b))
        if (a < b):
            a,b = b, a
        d = a % b
        if d != 0:
            a = d
        else:
            return b
            break

def gcd3(a, b):
    print("a= {}, b = {}".format(a, b))
    return gcd(b, a % b) if b else a

def main():
    a, b = map(int, input().split())
    print(gcd2(a, b))


if __name__ == "__main__":
    main()





# def fib_mod(n, m):
#     fibo = []
#     fibo.append(0)
#     fibo.append(1)
#
#     for i in range(2, n+1, 1):
#         fn = (fibo[i - 2] + fibo[i - 1]) % m
#
#         if (i > 6 and (fibo[i-1] == fibo[3] and fibo[i-2] ==fibo[2] and fibo[i-3] ==fibo[1])):
#             fibo = fibo[0:i-3]
#             break
#
#         fibo.append(fn)
#
#     i = n % (len(fibo)-1)
#
#     if (i>0):
#         return fibo[i]
#     else:
#         return fibo[-1]
#
#
#
# def main():
#     n, m = map(int, input().split())
#     print(fib_mod(n, m))
#
#
# if __name__ == "__main__":
#     main()
