def group_equal(lst):
    if len(lst) == 0:  # immediately return the list if it is empty..
        return lst

    else:
        result_lst = []
        first_cycle = True

        for el in lst:

            if first_cycle:  # create repetitions list, remember last el for next cycles
                repetitions = [el]
                last_el = el
                first_cycle = False
                continue

            if el != last_el:  # if it's not a repetition add rep. list to result
                result_lst.append(repetitions)
                repetitions = []

            repetitions.append(el)  # in end of each cycle add el to rep.list and remember last el
            last_el = el

        result_lst.append(repetitions)
        return result_lst

# print(group_equal([1, 1, 4, 4, 4, "hello", "hello", 4]) == [[1, 1], [4, 4, 4], ["hello", "hello"], [4]])
# print(group_equal([1, 2, 3, 4]) == [[1], [2], [3], [4]])
# print(group_equal([1,1]) == [[1,1]])
# print(group_equal([1]) == [[1]])
# print(group_equal([1,2]) == [[1],[2]])
# print(group_equal([]) == [])
