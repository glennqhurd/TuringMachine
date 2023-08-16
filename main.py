import itertools

# cipherCards are cards that are used to block specific entries on the solution to solve for the
# answer given three different color ciphers stacked.

# The top left 4 entries, bottom left 4 entries, and bottom right 3 entries are always blank.
# defaultCipher will provide a baseline. 'x' means incorrect answer.
defaultCipher = [['', '', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['', '', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                 ['', '', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', ''],
                 ['', '', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '', '']]

criteria = ((lambda b, y, p: b == 1, lambda b, y, p: b > 1),
            (lambda b, y, p: b < 3, lambda b, y, p: b == 3, lambda b, y, p: b > 3),
            (lambda b, y, p: y < 3, lambda b, y, p: y == 3, lambda b, y, p: b > 3),
            (lambda b, y, p: y < 4, lambda b, y, p: y == 4, lambda b, y, p: b > 4),
            (lambda b, y, p: b % 2 == 0, lambda b, y, p: b % 2 == 1),
            (lambda b, y, p: y % 2 == 0, lambda b, y, p: y % 2 == 1),
            (lambda b, y, p: p % 2 == 0, lambda b, y, p: p % 2 == 1),
            (lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 0, lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 1,
            lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 2, lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 3),
            (lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 0, lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 1,
            lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 2, lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 3),
            (lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 0, lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 1,
            lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 2, lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 3),
            (lambda b, y, p: b < y, lambda b, y, p: b == y, lambda b, y, p: b > y),
            (lambda b, y, p: b < p, lambda b, y, p: b == p, lambda b, y, p: b > p),
            (lambda b, y, p: y < p, lambda b, y, p: y == p, lambda b, y, p: y > p),
            (lambda b, y, p: b < y and b < p, lambda b, y, p: y < b and y < p, lambda b, y, p: p < b and p < y),
            (lambda b, y, p: b > y and b > p, lambda b, y, p: y > b and y > p, lambda b, y, p: p > b and p > y),
            (lambda b, y, p: (b % 2) + (y % 2) + (p % 2) > 1, lambda b, y, p: (b % 2) + (y % 2) + (p % 2) < 2),
            (lambda b, y, p: (b % 2) + (y % 2) + (p % 2) == 0, lambda b, y, p: (b % 2) + (y % 2) + (p % 2) == 1,
            lambda b, y, p: (b % 2) + (y % 2) + (p % 2) == 2, lambda b, y, p: (b % 2) + (y % 2) + (p % 2) == 3),
            (lambda b, y, p: (b + y + p) % 2 == 0, lambda b, y, p: (b + y + p) % 2 == 1),
            (lambda b, y, p: b + y < 6, lambda b, y, p: b + y == 6, lambda b, y, p: b + y > 6),
            (lambda b, y, p: len({b, y, p}) == 1, lambda b, y, p: len({b, y, p}) == 2,
            lambda b, y, p: len({b, y, p}) == 3),
            (lambda b, y, p: len({b, y, p}) != 2, lambda b, y, p: len({b, y, p}) == 2),
            (lambda b, y, p: b < y < p, lambda b, y, p: b > y > p, lambda b, y, p: not (b < y < p or b > y > p)),
            (lambda b, y, p: b + y + p < 6, lambda b, y, p: b + y + p == 6, lambda b, y, p: b + y + p > 6),
            (lambda b, y, p: b + 2 < y + 1 < p, lambda b, y, p: (b + 1 < y or y + 1 < p) and not b + 2 < y + 1 < p,
            lambda b, y, p: not (b + 1 < y or y + 1 < p)),
            # Question 25 (Ascending/Descending sequence)
            (lambda b, y, p: b + 2 < y + 1 < p or b > y + 1 > p + 2),
            lambda b, y, p: ((b + 1 < y or y + 1 < p) and not b + 2 < y + 1 < p) or
                            ((b > y + 1 or y > p + 1) and not b > y + 1 > p + 2),
            lambda b, y, p: not ((b + 1 < y or y + 1 < p) or (b > y + 1 or y > p + 1)),
            (lambda b, y, p: b + 1 != y and y + 1 != p),
            (lambda b, y, p: b < 3, lambda b, y, p: y < 3, lambda b, y, p: p < 3),
            (lambda b, y, p: b < 4, lambda b, y, p: y < 4, lambda b, y, p: p < 4),
            (lambda b, y, p: b == 1, lambda b, y, p: y == 1, lambda b, y, p: p == 1),
            (lambda b, y, p: b == 3, lambda b, y, p: y == 3, lambda b, y, p: p == 3),
            (lambda b, y, p: b == 4, lambda b, y, p: y == 4, lambda b, y, p: p == 4),
            (lambda b, y, p: b > 1, lambda b, y, p: y > 1, lambda b, y, p: p > 1),
            (lambda b, y, p: b > 3, lambda b, y, p: y > 3, lambda b, y, p: p > 3),
            (lambda b, y, p: b % 2 == 0, lambda b, y, p: b % 2 == 1, lambda b, y, p: y % 2 == 0,
            lambda b, y, p: y % 2 == 1, lambda b, y, p: p % 2 == 0, lambda b, y, p: p % 2 == 1),
            (lambda b, y, p: b <= y and b <= p, lambda b, y, p: y <= b and y <= p, lambda b, y, p: p <= b and p <= y),
            (lambda b, y, p: b >= y and b >= p, lambda b, y, p: y >= b and y >= p, lambda b, y, p: p >= b and p >= y),
            (lambda b, y, p: (b + y + p) % 3 == 0, lambda b, y, p: (b + y + p) % 4 == 0,
            lambda b, y, p: (b + y + p) % 5 == 0),
            (lambda b, y, p: b + y == 4, lambda b, y, p: b + p == 4, lambda b, y, p: y + p == 4),
            (lambda b, y, p: b + y == 4, lambda b, y, p: b + p == 4, lambda b, y, p: y + p == 4),
            (lambda b, y, p: b == 1, lambda b, y, p: b > 1, lambda b, y, p: y == 1, lambda b, y, p: y > 1,
            lambda b, y, p: p == 1, lambda b, y, p: p > 1),
            (lambda b, y, p: b < 3, lambda b, y, p: b == 3, lambda b, y, p: b > 3, lambda b, y, p: y < 3,
            lambda b, y, p: y == 3, lambda b, y, p: y > 3, lambda b, y, p: p < 3, lambda b, y, p: p == 3,
            lambda b, y, p: p > 3),
            (lambda b, y, p: b < 4, lambda b, y, p: b == 4, lambda b, y, p: b > 4, lambda b, y, p: y < 4,
            lambda b, y, p: y == 4, lambda b, y, p: y > 4, lambda b, y, p: p < 4, lambda b, y, p: p == 4,
            lambda b, y, p: p > 4),
            (lambda b, y, p: b < y and b < p, lambda b, y, p: y < b and y < p, lambda b, y, p: p < b and p < y,
            lambda b, y, p: b > y and b >= p, lambda b, y, p: y > b and y >= p, lambda b, y, p: p > b and p >= y),
            (lambda b, y, p: b < y, lambda b, y, p: b == y, lambda b, y, p: b > y, lambda b, y, p: b < p,
            lambda b, y, p: b == p, lambda b, y, p: b > p),
            (lambda b, y, p: y < b, lambda b, y, p: y == b, lambda b, y, p: y > b, lambda b, y, p: y < p,
            lambda b, y, p: y == p, lambda b, y, p: y > p),
            (lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 0, lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 1,
            lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 2, lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 0,
            lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 1, lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 2),
            (lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 0, lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 1,
            lambda b, y, p: (b == 3) + (y == 3) + (p == 3) == 2, lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 0,
            lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 1, lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 2),
            (lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 0, lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 1,
            lambda b, y, p: (b == 1) + (y == 1) + (p == 1) == 2, lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 0,
            lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 1, lambda b, y, p: (b == 4) + (y == 4) + (p == 4) == 2),
            (lambda b, y, p: b < y, lambda b, y, p: b == y, lambda b, y, p: b > y, lambda b, y, p: b < p,
            lambda b, y, p: b == p, lambda b, y, p: b > p, lambda b, y, p: y < p, lambda b, y, p: y == p,
            lambda b, y, p: y > p))


def stringToBaseFive(input):
    inputList = list(input)
    outputList = [(int(inputList[0]) - 1) * 25, (int(inputList[1]) - 1) * 5, int(inputList[2]) - 1]
    return sum(outputList)


# satisfies checks if the code tuple matches the result of the specific criterion
def satisfies(code, criterion):
    return criterion(int(code[0]), int(code[1]), int(code[2]))


# Check for multiple criteria at once then find if all succeed
def satisfies_all(code, criterion_list):
    for i in criterion_list:
        criterion1 = i[0]
        criterion2 = i[1]
        if satisfies(code, criteria[criterion1][criterion2]) is False:
            return False
    return True


def collect_unique_solutions(criteria_list):
    overall_solutions = []
    code_list = itertools.product(range(1, 6), range(1, 6), range(1, 6))
    criteria_product = itertools.product(criteria_list)
    for i in criteria_product:
        solution = []
        for j in code_list:
            if satisfies_all(j, i):
                solution.append([j, i])
        if len(solution) == 1:
            overall_solutions.append(solution)
    return overall_solutions


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(stringToBaseFive('111'))
    print(satisfies('311', criteria[1][1]))
    crit_list = [[0, 0], [1, 0], [2, 0]]
    print(satisfies_all('111', crit_list))
    print(collect_unique_solutions([4, 9, 11, 14]))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
