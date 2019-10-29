def checkio(string1, string2):
    word_in_both_string = []
    string1 = string1.split(',')  # make 2 lists
    string2 = string2.split(',')

    for word in string1:  # compare words with each other
        if word in string2:
            word_in_both_string.append(word)

    return ','.join(sorted(word_in_both_string))

# print(checkio("hello,world", "hello,earth") == "hello")
# print(checkio("one,two,three", "four,five,six") == "")
# print(checkio("one,two,three", "four,five,one,two,six,three") == "one,three,two")
