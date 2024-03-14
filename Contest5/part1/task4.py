'''
На шахматной доске стоят слоны и ладьи, необходимо посчитать, 
сколько клеток не бьется ни одной из фигур.

Шахматная доска имеет размеры 8 на 8. Ладья бьет все клетки горизонтали 
и вертикали, проходящих через клетку, где она стоит, до первой 
встретившейся фигуры. Слон бьет все клетки обеих диагоналей, 
проходящих через клетку, где он стоит, до первой встретившейся фигуры.
'''
# Входные данные:
# шахматная доска 8x8 (8 строк по 8 симолов), где:
# R - ладья
# B - слон
# * - пустая клетка
table = []
for _ in range(8):
    row = list(input())
    table.append(row)


# Алгоритм:
free_cells = 0

# Функция для проверки клетки на наличие фигуры и отметки
def mark_cell(i, j):
    v_cell = table[i][j]

    if v_cell in ('R', 'B'):
        return False

    if v_cell == '*':
        table[i][j] = 'X'

    return True

# Функции для проверки клеток, которые бьёт ладья
def check_rook(col_i, row_i):
    for i in range(row_i - 1, -1, -1):
        if not mark_cell(col_i, i):
            break

    for i in range(row_i + 1, 8):
        if not mark_cell(col_i, i):
            break

    for i in range(col_i - 1, -1, -1):
        if not mark_cell(i, row_i):
            break

    for i in range(col_i + 1, 8):
        if not mark_cell(i, row_i):
            break

# Функции для проверки клеток, которые бьёт слон
def check_bishop(col_i, row_i):
    for i in range(1, 8):
        if col_i - i < 0 or row_i - i < 0:
            break

        if not mark_cell(col_i - i, row_i - i):
            break

    for i in range(1, 8):
        if col_i + i >= 8 or row_i + i >= 8:
            break

        if not mark_cell(col_i + i, row_i + i):
            break

    for i in range(1, 8):
        if col_i - i < 0 or row_i + i >= 8:
            break

        if not mark_cell(col_i - i, row_i + i):
            break

    for i in range(1, 8):
        if col_i + i >= 8 or row_i - i < 0:
            break

        if not mark_cell(col_i + i, row_i - i):
            break

# Проверка клеток и отметка клеток, которые бьют фигуры
for h_i in range(8):
    for v_i in range(8):
        cell = table[h_i][v_i]
        if cell == 'R':
            check_rook(h_i, v_i)
        elif cell == 'B':
            check_bishop(h_i, v_i)

# Подсчёт свободных клеток
for h_i in range(8):
    for v_i in range(8):
        if table[h_i][v_i] == '*':
            free_cells += 1


# Выходные данные:
print(free_cells)
