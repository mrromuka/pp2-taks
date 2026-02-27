#1
def sqr(a):
    for i in range(1,a+1):
        yield i**2

a=int(input())
print(*sqr(a))
#2
def even_num(n):
    for  i in range (n+1):
        if i % 2 == 0 :
            yield i
a=int(input())
print(",".join(str(i) for i in even_num(a)))
#3
def div(n):
    for  i in range (n+1):
        if i % 12 == 0 :
            yield i
a=int(input())
print(*div(a))
#4
def pow1(n,m):
    for  i in range (n,m+1):  
         yield i**2
a,b=map(int, input().split())
print(*pow1(a,b))
#5
def countdown(n):
    for i in range(n, -1, -1): 
        yield i
n = int(input("Enter a number n: "))

for num in countdown(n):
    print(num, end=" ")






                 
                











