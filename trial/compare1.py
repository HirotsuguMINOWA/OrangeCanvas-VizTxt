import itertools

list_1 = [1, 5, 4]
# list_2 = [2,3,4]
list_2 = [1, 5]
# using list comprehensions
comparisons = [a == b for (a, b) in itertools.product(list_1, list_2)]
print("comparisons:", comparisons)
sums = [a + b for (a, b) in itertools.product(list_1, list_2)]
print("sum:", sums)
# using map and lambda
# comparisons = map(lambda (a, b): a == b, itertools.product(list_1, list_2))
# sums = map(lambda (a, b): a + b, itertools.product(list_1, list_2))

print("res:", [i == j for i, j in zip(list_1, list_2)])
