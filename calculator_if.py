while True:
    try:
        number_1=float(input())
        command =input()
        number_2 =float(input())
        if command == "*":
            print(number_1 * number_2)
        elif command == "-":
            print(number_1 - number_2)
        elif command == "+":
            print(number_1 + number_2)
        elif command == "**":
            print(number_1 ** number_2)
        elif command == "/":
            print(number_1 / number_2)
        elif command == "%":
            print(number_1 % number_2)
        elif command == "//":
            print(number_1 // number_2)
    except ZeroDivisionError:
        print('Division by Zero, take new number')
    except ValueError:
        print('I need a number')
