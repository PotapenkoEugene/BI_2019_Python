def checkio(x):
    dict = {}  # create a dict for define uniq elements of x
    uniq = []  # and list for uniq elements
    for el in x:    # define uniq elements in x
        if el in dict.keys():
            dict[el] += 1
        else:
            dict[el] = 1
    for key in dict.keys():  # create list with uniq elements of x
        if dict[key] == 1:
            uniq.append(key)
    result = [i for i in x if i not in uniq]  # generate list without uniq elements
    return result


# print(checkio([1, 2, 3, 4, 5]))
# print(checkio([1, 2, 3, 1, 3]))
# print(checkio([5, 5, 5, 5, 5]))
# print(checkio([10, 9, 10, 10, 9, 8]))
