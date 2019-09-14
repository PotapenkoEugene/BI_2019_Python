import __future__
while True:
    num_1 = input()
    operator = input()
    num_2 = input()
    try:
        lst_of_operators = ['/','+','-','*','**','//','%']
        if operator in lst_of_operators:
            print(eval(compile(num_1 + ' ' + operator + ' ' + num_2, "<string>",'eval', __future__.division.compiler_flag)))
    # eval() без compile() выдавал ответы при делении в формате int
        else:
            print('Incorrect operator')
    except ZeroDivisionError:
        print('Division by Zero')
    except ValueError:
        print('Need a number')



