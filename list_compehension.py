# 1. Составить список из чисел от 1 до 1000, которые имеют в своём составе 7.
ex_1 = [num for num in range(1, 1001) if '7' in str(num)]
print('Ex1:', ex_1)

# 2. Взять предложение **Would it save you a lot of time if I just gave up and went mad now?** и
# сделать его же без гласных. **up:** можно оставить в виде списка слов и не собирать строку.
sentence = 'Would it save you a lot of time if I just gave up and went mad now?'
ex_2 = [letter for letter in sentence if letter.upper() not in ['A', 'E', 'I', 'U', 'Y', 'O']]
# print(ex_2)

# Let's join in it in sentence
words = []
word = []
for letter in ex_2:
    if letter != ' ':
        word.append(letter)
    elif word:
        words.append(''.join(word))
        word = []
print('Ex2:', ' '.join(words))

# 3. Для предложения **The ships hung in the sky in much the same way that bricks don't**
# составить словарь, где слову соответствует его длина.
sentence = 'The ships hung in the sky in much the same way that bricks don\'t'
words = sentence.split()
ex_3 = dict(zip(words, [len(word) for word in words]))
print('Ex3:', ex_3)

# 4*. Для чисел от 1 до 1000 наибольшая цифра, на которую они делятся (1-9).
ex_4 = [max([divider for divider in range(1, 10) if num % divider == 0]) for num in range(1, 1001)]
print('Ex4:', ex_4)

# 5*. Список всех чисел от 1 до 1000, не имеющих делителей среди чисел от 2 до 9.
ex_5 = [num for num in range(1, 1001) if (num % 2 != 0) and (num % 9 != 0)]
print('Ex5:', ex_5)
