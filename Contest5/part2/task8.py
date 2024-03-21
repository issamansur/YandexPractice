'''
Константин и Михаил играют в настольную игру «Ярость Эльфов». 
В игре есть n рас и m классов персонажей. Каждый персонаж характеризуется 
своими расой и классом. Для каждой расы и каждого класса существует ровно 
один персонаж такой расы и такого класса. Сила персонажа i-й расы и j-го 
класса равна ai j, и обоим игрокам это прекрасно известно.

Сейчас Константин будет выбирать себе персонажа. Перед этим Михаил 
может запретить одну расу и один класс, чтобы Константин не мог выбирать 
персонажей, у которых такая раса или такой класс. Конечно же, Михаил 
старается, чтобы Константину достался как можно более слабый персонаж, 
а Константин, напротив, выбирает персонажа посильнее. Какие расу и класс 
следует запретить Михаилу?
'''
# Входные данные:
# N, M - количество рас и классов персонажей
N, M = map(int, input().split())

# Алгоритм:
# Создаём массив для хранения силы персонажей
arr = []

# Максимальные два значения силы персонажей
max_1_value = 0
max_1_row_index = 0
max_1_column_index = 0

max_2_value = 0
max_2_row_index = 0
max_2_column_index = 0

for i in range(N):
    # Считываем силу персонажей
    row = list(map(int, input().split()))
    arr.append(row)

    # Сразу находим два максимальных значения и их индексы
    for j in range(M):
        value = row[j]
        if value > max_1_value:
            max_2_value = max_1_value
            max_2_row_index = max_1_row_index
            max_2_column_index = max_1_column_index

            max_1_value = value
            max_1_row_index = i
            max_1_column_index = j
        elif value > max_2_value:
            max_2_value = value
            max_2_row_index = i
            max_2_column_index = j

# Зануляем максимальные значения, чтобы не мешались
arr[max_1_row_index][max_1_column_index] = 0
arr[max_2_row_index][max_2_column_index] = 0

# Теперь всё зависит от взаимного расположения максимальных значений
max_3_value = 0
max_3_row_index = 0
max_3_column_index = 0

if max_1_row_index == max_2_row_index:
    for i in range(N):
        if i == max_1_row_index:
            continue
        for j in range(M):
            value = arr[i][j]
            if value > max_3_value:
                max_3_value = value
                max_3_row_index = i
                max_3_column_index = j

    print(max_1_row_index + 1, max_3_column_index + 1)

elif max_1_column_index == max_2_column_index:
    for j in range(M):
        if j == max_1_column_index:
            continue
        for i in range(N):
            value = arr[i][j]
            if value > max_3_value:
                max_3_value = value
                max_3_row_index = i
                max_3_column_index = j

    print(max_3_row_index + 1, max_1_column_index + 1)

else:
    for i in [max_1_row_index, max_2_row_index]:
        for j in range(M):
            value = arr[i][j]
            if value > max_3_value:
                max_3_value = value
                max_3_row_index = i
                max_3_column_index = j

    for j in [max_1_column_index, max_2_column_index]:
        for i in range(N):
            value = arr[i][j]
            if value > max_3_value:
                max_3_value = value
                max_3_row_index = i
                max_3_column_index = j

    if max_3_row_index == max_1_row_index:
        print(max_3_row_index + 1, max_2_column_index + 1)
    elif max_3_row_index == max_2_row_index:
        print(max_3_row_index + 1, max_1_column_index + 1)
    elif max_3_column_index == max_1_column_index:
        print(max_2_row_index + 1, max_3_column_index + 1)
    else:
        print(max_1_row_index + 1, max_3_column_index + 1)

# Примечание к решению после нахождения двух максимальных значений:

# 1. Если они находятся в одной строке, то эту строку нужно запретить в
# любом случае, так как в ней находится два максимальных значения.
# А столбец нужно запретить так, чтобы вычеркнулось ещё одно максимальное
# возможное значение.

# 2. Если они находятся в одном столбце, то аналогично пункту 1, только
# столбец нужно запретить, а строку - так, чтобы вычеркнулось ещё одно
# максимальное возможное значение.

# 3. Если они находятся в разных строках и столбцах
# То Михаилу нужно запретить одно из пересечений строк и столбцов так,
# чтобы при вычёркивании столбца и строки вычеркнулось ещё одно
# возможное максимальное значение
# Пример:
# 1 3 5 7
# 9 11 2 4
# 6 8 10 12
# Максимальные значения: 12 и 11, запретить можем 3 строку и 2 столбец
# или 2 строку и 4 столбец. Но в первом случае вычеркивается 10, а во
# втором 9. Поэтому нужно запретить 3 строку и 2 столбец.
