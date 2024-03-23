'''
Недавно один известный художник-абстракционист произвел на свет новый
шедевр — картину «Два черных непересекающихся прямоугольника». Картина 
представляет собой прямоугольник m× n, разбитый на квадраты 1× 1, 
некоторые из которых закрашены любимым цветом автора — черным. Федя — 
не любитель абстрактных картин, однако ему стало интересно, действительно 
ли на картине изображены два непересекающихся прямоугольника. 
Помогите ему это узнать. Прямоугольники не пересекаются в том смысле, 
что они не имеют общих клеток.
'''

# Входные данные:
# M, N - количество строк и столбцов в таблице
M, N = map(int, input().split())

# Класс прямоугольника
class Rectangle:
    IS_ENDED = False
    SYMBOL = 'a'

    def __init__(self, X=0, Y=0, width=0, height=0):
        self.X = X
        self.Y = Y
        self.width = width
        self.height = height

    def plus_height(self):
        self.height += 1

    def lock(self):
        self.IS_ENDED = True

    def change_symbol(self):
        self.SYMBOL = 'b'

    def __eq__(self, other):
        return self.X == other.X and self.width == other.width and not (self.IS_ENDED or other.IS_ENDED)

    def __str__(self) -> str:
        return f'X: {self.X}, width: {self.width}, Y: {self.height} height: {self.height}, IS_ENDED: {self.IS_ENDED}, SYMBOL: {self.SYMBOL}'

IS_ONE_MORE = False
NUMBER = 0

result = []
last_row = ""
rectangles = []

# Алгоритм:
for Y in range(M):
    current_rectangles = []

    row = input().strip()
    if row != last_row:
        last_row = row
        START_INDEX = -1

        for (index, char) in enumerate(row + '.'):
            if char == '#' and START_INDEX == -1:
                START_INDEX = index
            elif char != '#' and START_INDEX != -1:
                current_rectangles.append(
                    Rectangle(START_INDEX, Y, index - START_INDEX - 1)
                )
                START_INDEX = -1

                if len(current_rectangles) > 1:
                    current_rectangles[-1].change_symbol()
        if len(current_rectangles) > 2:
            NUMBER = 3
        elif len(current_rectangles) == 2 and NUMBER == 2:
            NUMBER = 3
        elif len(current_rectangles) == 2 and NUMBER == 1:
            if rectangles[0] == current_rectangles[0]:
                rectangles.append(
                    current_rectangles[1]
                )
            elif rectangles[0] == current_rectangles[1]:
                rectangles.append(
                    current_rectangles[0]
                )
            else:
                NUMBER = 3
                continue

            rectangles[0].plus_height()
            rectangles[1].change_symbol()
            NUMBER += 1
        elif len(current_rectangles) == 2 and NUMBER == 0:
            NUMBER += 2
            rectangles = current_rectangles
        elif len(current_rectangles) == 1 and NUMBER == 2:
            if current_rectangles[0] == rectangles[0]:
                rectangles[0].plus_height()
                rectangles[1].lock()
            elif current_rectangles[0] == rectangles[1]:
                rectangles[1].plus_height()
                rectangles[0].lock()
            else:
                NUMBER = 3
        elif len(current_rectangles) == 1 and NUMBER == 1:
            print(*rectangles)
            print(*current_rectangles)
            if rectangles[0].X == current_rectangles[0].X and rectangles[0].width < current_rectangles[0].width:
                rectangles[0].plus_height()
                rectangles.append(
                    Rectangle(rectangles[0].X + rectangles[0].width + 1, Y, current_rectangles[0].width - rectangles[0].width - 1)
                )
                rectangles[-1].change_symbol()
            elif current_rectangles[0].X < rectangles[0].X and rectangles[0].X + rectangles[0].width == current_rectangles[0].X + current_rectangles[0].width:
                rectangles[0].plus_height()
                rectangles.insert(
                    0,
                    Rectangle(current_rectangles[0].X, Y, current_rectangles[0].width - rectangles[0].width - 1)
                )
                rectangles[0].change_symbol()
            else:
                rectangles[0].lock()
                rectangles.append(
                    current_rectangles[0]
                )
                rectangles[-1].change_symbol()
            NUMBER += 1
        elif len(current_rectangles) == 1 and NUMBER == 0:
            NUMBER += 1
            rectangles.append(
                current_rectangles[0]
            )
        else:
            for rectangle in current_rectangles:
                rectangle.lock()
    else:
        for rectangle in rectangles:
            if not rectangle.IS_ENDED:
                rectangle.plus_height()

    sort_rectangles = [rectangle for rectangle in rectangles if not rectangle.IS_ENDED]
    if len(sort_rectangles) == 2:
        result.append(
            row
                .replace('#', rectangles[0].SYMBOL, rectangles[0].width + 1)
                .replace('#', rectangles[1].SYMBOL, rectangles[1].width + 1)
            )
    elif len(sort_rectangles) == 1:
        result.append(row.replace('#', sort_rectangles[0].SYMBOL, sort_rectangles[0].width + 1))
    else:
        result.append(row)

# Выходные данные:
if NUMBER == 2:
    print('YES')
    print(*result, sep='\n')
elif NUMBER == 1:
    if rectangles[0].height > 0:
        result[rectangles[0].Y + rectangles[0].height] = result[rectangles[0].Y + rectangles[0].height].replace('a', 'b', rectangles[0].width + 1)
        print('YES')
        print(*result, sep='\n')
    elif rectangles[0].width > 0:
        result[rectangles[0].Y] = result[rectangles[0].Y].replace('a', 'b', 1)
        print('YES')
        print(*result, sep='\n')
    else:
        print('NO')
else:
    print('NO')
