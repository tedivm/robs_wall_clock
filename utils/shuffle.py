from random import randrange


def shuffle(lst):
    for i in range(len(lst)):
        j = randrange(0, len(lst))
        lst[i], lst[j] = lst[j], lst[i]
