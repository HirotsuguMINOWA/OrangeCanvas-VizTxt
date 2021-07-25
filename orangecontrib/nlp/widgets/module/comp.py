import itertools
import time
from typing import List


# TODO: logger置き換えろ
def comp(l_user: List[List[str]], target_pos: List[str]):
    """

    :param l_user: ユーザが指定した抽出したいPOSが記載されたlist
    :param target_pos:
    :return: ユーザ指定したPOSリストに一致した場合Trueを返す
    """
    for l_usr1 in l_user:
        # n = len(l_usr1)
        if len(l_usr1) <= len(target_pos):
            res = [i == j for i, j in zip(l_usr1, target_pos)]  # 不可、リスト長の短い方に合わせてしまう。遅い、しかし、同一要素番号を比較するのはこれしか思いつかない
            # res = [True for i, e in enumerate(l_usr1) if target_pos[i] == e]
            # print("res:", res)
            # res2 = all(res[:n])
            # if all(res[:n]):
            if all(res):
                return True
    return False


if __name__ == '__main__':
    list_1 = [1, 5, 4]
    # list_2 = [2,3,4]
    list_2 = [1, 4]

    start = time.perf_counter()
    print("comp1:", comp([[1, 3], [2, 1], [1, 3]], list_1))
    print(time.perf_counter() - start)
    #
    # using list comprehensions
    #
    start = time.perf_counter()
    comparisons = [a == b for (a, b) in itertools.product(list_1, list_2)]  # 早い
    print(time.perf_counter() - start)
    print("comparisons:", comparisons)
    # sums = [a + b for (a, b) in itertools.product(list_1, list_2)]
    # print("sum:", sums)
    # using map and lambda
    # comparisons = map(lambda (a, b): a == b, itertools.product(list_1, list_2))
    # sums = map(lambda (a, b): a + b, itertools.product(list_1, list_2))

    # print(frozenset(list_1).intersection(list_2))
    #
    #
    # def compare_bitwise(x, y):
    #     set_x = frozenset(x)
    #     set_y = frozenset(y)
    #     return set_x & set_y
    #
    #
    # print(compare_bitwise(list_1, list_2))
