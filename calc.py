a = int(input())
op = input()
b = int(input())
if op =='/' and b == 0:
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
