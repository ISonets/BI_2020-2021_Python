# simple calculator, homework №1
a = int(input())  # first number
op = input()  # operation
b = int(input())  # second number
if op == '/' and b == 0:
    print('На ноль делить нельзя!')
elif op == '/' and b != 0:
    print(a / b)
elif op == '*':
    print(a * b)
elif op == '+':
    print(a + b)
elif op == '-':
    print(a - b)
else:
    print('Неверная операция')
