def create_intervals(set_data):
    if len(set_data) == 0 or not all(isinstance(x, int) for x in set_data):
        return None  # return None if incorrect input

    first_cycle = True
    nums = []
    result = []

    for num in set_data:

        if first_cycle:
            last_num = num  # remember last el for next cycles..
            first_cycle = False
            nums.append(num)
            continue

        if last_num == num - 1:  # if it's next num, add it to nums
            nums.append(num)
            last_num = num
        else:  # if it's not next num add interval to result
            result.append((min(nums), max(nums)))
            last_num = num
            nums = [num]

    result.append((min(nums), max(nums)))  # add last interval
    return result

# print(create_intervals({1, 2, 3, 4, 5, 7, 8, 12}) == [(1, 5), (7, 8), (12, 12)])
# print(create_intervals({1, 2, 3, 6, 7, 8, 4, 5}) == [(1, 8)])
# print(create_intervals({1,'2'}) != [(1,2)])
