def flat_list(lst):
    if type(lst) == str or type(lst) == dict:   # work with all iter except str, dict
        return None
    one_dim_list = []
    try:
        for i in lst:
            if hasattr(i, '__iter__'):
                one_dim_list += flat_list(i)
            else:
                one_dim_list.append(i)
        return one_dim_list
    except TypeError:   # initial argument must be iter
        return None

# print(flat_list([{1,2,3},(4,5), 6,77]))
# print(flat_list([[1,[2,[3,[4,[5]]]]]]))
# print(flat_list([[[2]], [4, [5, 6, [6], 6, 6, 6], 7]]))
# print(flat_list([-1, [1, [-2], 1], -1]))
# print(flat_list(1))
# print(flat_list('ghgsh'))
# print(flat_list({1:2,3:4,5:6}))