import __future__
from typing import List

while True:
    try:
        num_1 = float(input())
        operator = input()
        num_2 = float(input())
        lst_of_operators: List[str] = ['/', '+', '-', '*', '**', '//', '%']
        if operator in lst_of_operators:
            print(eval(
                compile(str(num_1) + ' ' + operator + ' ' + str(num_2), "<string>", 'eval', __future__.division.compiler_flag)))
        # eval() без compile() выдавал ответы при делении в формате int
        else:
            print('Incorrect operator')
    except ZeroDivisionError:
        print('Division by Zero')
    except ValueError:
        print('Need a number')
