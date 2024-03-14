'''
Вы играете в интересную стратегию. 
У вашего соперника остались всего одна казарма — здание, 
в котором постоянно появляются новые солдаты. 
Перед атакой у вас есть x солдат. 
За один раунд каждый солдат может убить одного из солдат противника 
или нанести 1 очко урона казарме (вычесть единицу здоровья у казармы). 
Изначально у вашего оппонента нет солдат. Тем не менее, его казарма имеет 
y единиц здоровья и производит p солдат за раунд.

Ход одного раунда:
1. Каждый солдат из вашей армии либо убивает одного из солдат 
вашего противника, либо наносит 1 очко урона казарме. 
Каждый солдат может выбрать своё действие. 
Когда казарма теряет все свои единицы здоровья, она разрушается.

2. Ваш противник атакует. Он убьет k ваших солдат, 
где k — количество оставшихся у противника солдат.

3. Если казармы еще не разрушены, ваш противник производит p новых солдат.

Ваша задача — разрушить казарму и убить всех солдат противника. 
Если это возможно, посчитайте минимальное количество раундов, 
которое вам нужно для этого. В противном случае выведите -1.
'''

from math import floor

# Константы:
# Число Фибоначчи или золотое сечение
COEFFICIENT = 1.61803398875
# Числа Фибоначчи 1 1 2 3 5 8 13 21 34 55 89 144 (их отношение)
fibb = [1/1, 2/3, 5/8, 13/21, 34/55, 89/144]

# Входные данные:
# x - количество солдат у вас
# y - количество здоровья казармы у противника
# z - количество солдат, которое производит казарма противника
x = int(input())
y = int(input())
z = int(input())


# Алгоритм:
def get_steps_number(xx, yy, zz):
    # 1 Победа ли в первом ходе?
    if yy <= xx:
        yy -= yy
        return 1

    yy -= xx
    k = 1

    # 2 Ломаем бараки до тех пор, пока не станет выгодно
    if xx <= zz and xx * COEFFICIENT < yy + zz:
        return -1

    if xx >= yy + zz:
        return k + 1

    # Золотое сечение
    # 1.618 * x >= y - n * (x - z) + z
    # (y + z - 1.618 * x) / (x - z) <= n
    if xx > zz and yy + zz > COEFFICIENT * xx:
        n = floor((yy + zz - COEFFICIENT * xx) / (xx - zz)) + 1
        k += n
        yy -= n * (xx - zz)

    print(f"{xx} {yy} {zz} (Ход {k})")
    print("Уже выигрышная ситуация")

    if xx >= yy + zz:
        return k + 1

    # 3 Ломаем барак сейчас или ждем ещё ход?
    zz_next_break = zz - (xx - yy)
    xx_next_break = xx - zz_next_break

    yy_next_no_break = yy - (xx - zz)

    if zz_next_break == 0:
        return k + 1

    if xx_next_break / (0 + zz_next_break) < xx / (yy_next_no_break + zz):
        print("Ждём ещё ход")
        k += 1
        yy -= xx - zz
        print(f"{xx} {yy} {zz} (Ход {k})")


    # 4 Ломаем барак
    if xx >= yy + zz:
        return k + 1

    print("Ломаем барак")
    zz -= xx - yy
    yy = 0
    xx -= zz
    k += 1
    print(f"{xx} {yy} {zz} (Ход {k})")

    # 5 Бьёмся до победного конца
    # Формула Бине (не решено) / числа Фибоначчи (решено)
    # F_n = [phi^n / sqrt(5)]
    # F_n+1 = [phi^(n+1) / sqrt(5)]
    # F_n / F_n+1 = [phi^n / sqrt(5)] / [phi^(n+1) / sqrt(5)]
    # xx / zz = [phi^(n+1) / sqrt(5)] / [phi^n / sqrt(5)]

    if xx >= zz:
        print(f"Победа! (Ход {k + 1})")
        return k + 1

    for (i, koef) in enumerate(fibb):
        if  xx / zz >= koef:
            n = i
            break
    k += n

    print(f"Победа! (Ход {k + 1})")

    return k + 1

res = get_steps_number(x, y, z)

# Выходные данные:
print(res)
