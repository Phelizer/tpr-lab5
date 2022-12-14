import math
import numpy as np

# CRITERIA_WEIGHTS
W = [9, 10, 3, 7, 6, 2, 5, 7, 7, 1, 10, 1]

# ESTIMATIONS
X = [[9, 4, 7, 7, 10, 9, 4, 5, 8, 3, 1, 1],
     [7, 8, 3, 2, 2, 8, 8, 8, 5, 9, 1, 3],
     [1, 4, 1, 10, 6, 7, 5, 10, 5, 10, 5, 2],
     [4, 10, 9, 8, 9, 7, 2, 6, 4, 10, 2, 9],
     [4, 2, 6, 1, 6, 9, 7, 3, 6, 1, 2, 4],
     [5, 1, 3, 2, 2, 6, 1, 5, 7, 3, 5, 1],
     [5, 10, 3, 6, 9, 2, 4, 9, 4, 1, 9, 1],
     [4, 1, 4, 6, 9, 7, 3, 4, 5, 10, 9, 2],
     [5, 4, 6, 3, 1, 7, 4, 7, 5, 6, 9, 6],
     [8, 3, 6, 7, 1, 9, 8, 6, 4, 7, 6, 10],
     [4, 4, 2, 6, 10, 4, 2, 3, 6, 7, 8, 9],
     [2, 2, 1, 9, 2, 7, 3, 8, 9, 4, 3, 3],
     [1, 4, 1, 2, 9, 4, 3, 8, 9, 7, 6, 5],
     [6, 10, 6, 1, 3, 7, 10, 9, 10, 7, 10, 8],
     [9, 6, 1, 8, 4, 2, 9, 2, 5, 8, 10, 8]]


# NORMALIZED WEIGHTS
def w(j: int) -> float:
    return W[j] / sum(W)


# # NORMALIZED ESTIMATIONS
# def r(k: int, j: int) -> float:
#     return X[k][j]/math.sqrt(sum(map(lambda x: x ** 2, column(j))))


def column(j: int) -> list:
    return [X[k][j] for k in range(len(X))]


# NORMALIZED ESTIMATIONS
def rBenefit(k: int, j: int) -> float:
    return (X[k][j] - min(column(j)))/(max(column(j)) - min(column(j)))


def rCost(k: int, j: int) -> float:
    return (min(column(j)) - X[k][j])/(min(column(j)) - max(column(j)))


# WEIGHTED NORMALIZED ESTIMATIONS
def v(k: int, j: int, criteriasToMaximize: list[int]) -> float:
    return w(j)*(rBenefit(k, j) if j in criteriasToMaximize else rCost(k, j))

# def PIS(j: int) -> list[float]:


def APlus(j: int, criteriasToMaximize: list[int]) -> float:
    vs = list(map(lambda k: v(k, j, criteriasToMaximize), range(len(X))))
    return max(vs) if j in criteriasToMaximize else min(vs)


def AMinus(j: int, criteriasToMaximize: list[int]) -> float:
    vs = list(map(lambda k: v(k, j, criteriasToMaximize), range(len(X))))
    return min(vs) if j in criteriasToMaximize else max(vs)


def DPlus(k: int, criteriasToMaximize: list[int]) -> float:
    return sum(map(lambda j: (v(k, j, criteriasToMaximize) - APlus(j, criteriasToMaximize)) ** 2, range(len(W)))) ** 0.5


def DMinus(k: int, criteriasToMaximize: list[int]) -> float:
    return sum(map(lambda j: (v(k, j, criteriasToMaximize) - AMinus(j, criteriasToMaximize)) ** 2, range(len(W)))) ** 0.5


def C(k: int, criteriasToMaximize: list[int]) -> float:
    return DMinus(k, criteriasToMaximize)/(DMinus(k, criteriasToMaximize) + DPlus(k, criteriasToMaximize))


def rank(criteriasToMaximize: list[int]) -> list[int]:
    return sorted(range(len(X)), key=lambda k: C(k, criteriasToMaximize), reverse=True)


def increment(lst: list[int]) -> list[int]:
    return list(map(lambda x: x + 1, lst))


print("Criterias to maximize:, ", increment(list(range(len(W)))))
print(increment(rank(list(range(len(W))))))

print("Criterias to maximize:, ", increment(list(range(7))))
print(increment(rank(list(range(7)))))


# VIKOR

def fBest(j: int) -> float:
    return max(column(j))


def fWorst(j: int) -> float:
    return min(column(j))


def S(k: int) -> float:
    return sum(map(lambda j: (w(j) * abs(fBest(j) - X[k][j])) / abs(fBest(j) - fWorst(j)), range(len(W))))


def R(k: int) -> float:
    return max(map(lambda j: (w(j) * abs(fBest(j) - X[k][j])) / abs(fBest(j) - fWorst(j)), range(len(W))))


def SPlus() -> float:
    return min(map(lambda k: S(k), range(len(X))))


def SMinus() -> float:
    return max(map(lambda k: S(k), range(len(X))))


def RPlus() -> float:
    return min(map(lambda k: R(k), range(len(X))))


def RMinus() -> float:
    return max(map(lambda k: R(k), range(len(X))))


def Q(k: int, v: float) -> float:
    return v*(S(k) - SPlus())/(SMinus() - SPlus()) + (1 - v)*(R(k) - RPlus())/(RMinus() - RPlus())


def rankByQ(v: float) -> list[float]:
    return sorted(range(len(X)), key=lambda k: Q(k, v), reverse=True)


def rankByS() -> list[float]:
    return sorted(range(len(X)), key=lambda k: S(k), reverse=True)


def rankByR() -> list[float]:
    return sorted(range(len(X)), key=lambda k: R(k), reverse=True)


def DQ(n: int) -> float:
    return 1/(n-1)


def C1(kBest: int, kSecondBest: int, v: float) -> bool:
    return Q(kSecondBest, v) - Q(kBest, v) >= DQ(len(X))


def C2(kBest: int) -> bool:
    return rankByS()[-1] == kBest and rankByR()[-1] == kBest


def vikor(v: float):
    print(rankByQ(v))


def compromise(v: float):
    kBest = rankByQ(v)[-1]
    kSecondBest = rankByQ(v)[-2]

    if C1(kBest, kSecondBest, v) and C2(kBest):
        return [kBest]

    if (C1(kBest, kSecondBest, v)):
        return [kBest, kSecondBest]

    result = []
    for k in range(len(X)):
        if Q(k, v) - Q(kBest, v) >= DQ(len(X)):
            break

        result.append(k)

    return result


# print('Vikor output:')
# print('v =', 0.5)
# print('ranged by Q', increment(rankByQ(0.5)))
# print('ranged by R', increment(rankByR()))
# print('ranged by S', increment(rankByS()))
# print('compromise', increment(compromise(0.5)))

# print('\n')
# print('Changing v from 0 to 1:')
# for v_ in np.arange(0, 1.1, 0.1):
#     print('v =', v_)
#     print('ranged by Q', increment(rankByQ(v_)))
#     print('ranged by R', increment(rankByR()))
#     print('ranged by S', increment(rankByS()))
#     print('compromise', increment(compromise(v_)))
#     print('\n')
