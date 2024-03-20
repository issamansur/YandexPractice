'''
Дан массив целых положительных чисел a длины n. Разбейте его на минимально
возможное количество отрезков, чтобы каждое число было не меньше длины
отрезка которому оно принадлежит. Длиной отрезка считается количество
чисел в нем.

Разбиение массива на отрезки считается корректным, если каждый элемент
принадлежит ровно одному отрезку.
'''

# Входные данные:
# T - количество тестов
T = int(input())

# Список сегментов
segments = []

for _ in range(T):
    _ = int(input())
    segment = list(map(int, input().split()))
    segments.append(segment)

# Алгоритм:
for segment in segments:
    lengths = []
    length = 0
    min_point = segment[0]

    i = 0
    len_segment = len(segment)
    while i < len_segment:
        length += 1
        point = segment[i]
        if point < min_point:
            min_point = point
        if min_point < length:
            lengths.append(length - 1)
            length = 1
            min_point = segment[i]
        i += 1
    lengths.append(length)

    # Выходные данные:
    print(len(lengths))
    print(lengths)
