import copy

def merge(lhs, rhs):
    ret = []

    for elem in lhs:
        if elem < rhs[0]:
            ret.append(elem)
        else:
            while rhs and rhs[0] < elem:
                ret.append(rhs[0])
                rhs = rhs[1:]
            ret.append(elem)

    if rhs:
        ret += rhs

    return ret


def merge_sort(lst):
    # breakpoint()
    if len(lst) == 1:
        return lst
    elif len(lst) == 2:
        return [min(lst[0], lst[1]), max(lst[0], lst[1])]
    else:
        half = len(lst) // 2
        lhs = lst[:half]
        rhs = lst[half:]
        lhs = merge_sort(lhs)
        rhs = merge_sort(rhs)
        return merge(lhs, rhs)

lst = [5, 3, 2, 7, 9, 1,3 ,8]
print(merge_sort(copy.deepcopy(lst)))

