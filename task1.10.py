class ReaderObj:
    '''
    Базовый класс для всех объектов, которые могут быть в тексте.

    Атрибуты:
    pos_x (int): координата x левого верхнего угла объекта
    pos_y (int): координата y левого верхнего угла объекта
    width (int): ширина объекта
    height (int): высота объекта
    '''
    pos_x = 0
    pos_y = 0
    width = 0
    height = 0

    def set_position(self, x: int, y: int):
        '''
        Устанавливает позицию объекта.
        '''
        self.pos_x = x
        self.pos_y = y

class Paragraph(ReaderObj):
    '''
    Класс для абзаца.

    Используется для картинок типа "floating". 
    (Ведь при этом картинка ориентируется на абзац, а не на слово.)
    '''
    def __init__(self, pos_y: int = 0):
        self.pos_y = pos_y

    def __str__(self):
        return f'Paragraph: y={self.pos_y}'

class Word(ReaderObj):
    '''
    Класс для слова.

    Высота слова всегда равна высоте символа.
    Длина слова равна количеству символов, умноженному на ширину символа.
    '''
    def __init__(self, word: str):
        self.width = len(word) * c
        self.height = h

    def __str__(self):
        return f'Word: x={self.pos_x} y={self.pos_y}'

class Image(ReaderObj):
    '''
    Класс для изображения.

    embeded - изображение встроено в текст
    surrounded - изображение окружено текстом
    floating - изображение плавающее

    Дополнительные атрибуты:
    layout (str): тип размещения изображения (embedded, surrounded, floating)
    dx (int): смещение по оси x для floating
    dy (int): смещение по оси y для floating
    '''
    def __init__(self, layout="embeded", width=0, height=0, dx=0, dy=0):
        self.layout = layout
        self.width = width
        self.height = height
        self.dx = dx
        self.dy = dy

    def set_param_from_str(self, string: str):
        '''
        Устанавливает параметры из строки вида "param=value".
        '''
        param, value = string.split('=')
        if param == 'layout':
            self.layout = value
        elif param == 'width':
            self.width = int(value)
        elif param == 'height':
            self.height = int(value)
        elif param == 'dx':
            self.dx = int(value)
        elif param == 'dy':
            self.dy = int(value)

    def __str__(self):
        string = f'Image: layout={self.layout} width={self.width} height={self.height}'
        if self.layout == 'floating':
            return string + f' dx={self.dx} dy={self.dy}'
        return string


class Reader:
    '''
    Класс для чтения текста.
    
    Атрибуты:
    page_width (int): ширина страницы
    char_width (int): ширина символа
    char_height (int): высота символа
    pos_x (int): текущая координата x

    pos_y_min (int): минимальная координата y текущей строки
    pos_y_max (int): максимальная координата y текущей строки

    LAST_OBJ (ReaderObj): последний объект
    IS_START_OF_FRAGMENT (bool): начало фрагмента текста
    surroundeds (list): список окруженных изображений
    '''
    page_width = 0
    char_width = 0
    char_height = 0

    pos_x = 0
    pos_y_min = 0
    pos_y_max = 0

    last_obj: ReaderObj = None
    is_start_of_fragment = True
    surroundeds = []

    def __init__(self, page_width: int, char_width: int, char_height: int):
        self.page_width = page_width
        self.char_width = char_width
        self.char_height = char_height
        self.pos_y_max = char_height

        self.last_obj = Paragraph(self.pos_y_min)
        self.is_start_of_fragment = True

    def space(self):
        '''
        Добавляет пробел.
        '''
        self.pos_x += c

    def new_line(self):
        '''
        Переходит на новую строку.
        '''
        self.pos_x = 0
        self.pos_y_min = self.pos_y_max
        self.pos_y_max = self.pos_y_min + h

    def paragraph(self):
        '''
        Добавляет абзац.
        
        1. Сбрасываем координату x.
        2. Если есть окруженные изображения, то находим максимальную 
        координату У среди них. 
        Иначе берём текущую максимальную координату.
        3. Устанавливаем минимальную координату y текущей строки,
        увеличивая найденную минимальную координату на высоту символа.
        '''
        self.pos_x = 0
        if len(self.surroundeds) > 0:
            y_min = max(self.pos_y_max, *[y for _, _, y in self.surroundeds])
        else:
            y_min = self.pos_y_max
        self.pos_y_min = y_min
        self.pos_y_max = y_min + self.char_height

        self.last_obj = Paragraph(self.pos_y_min)
        self.is_start_of_fragment = True

    def set_object(self, obj: ReaderObj):
        '''
        Устанавливает объект на странице в свободном месте.

        1. Если объект не помещается на текущей строке, 
        то переходим на новую строку.
        2. Перемещаем курсор вправо.
        3. Если объект пересекается с окруженными изображениями,
        то перемещаем курсор вправо до конца пересечения.
        4. Если объект не пересекается с окруженными изображениями,
        то устанавливаем его на странице. Иначе переходим к пункту 1.
        '''
        while True:
            if self.pos_x + obj.width > self.page_width:
                self.new_line()

            self.pos_x += obj.width

            intersections = list(
                filter(
                    lambda surr:
                        (self.pos_x - 1 in range(surr[0], surr[1])
                        or surr[1] - 1 in range(self.pos_x - obj.width, self.pos_x))
                        and self.pos_y_min < surr[2],
                    self.surroundeds
                )
            )

            if len(intersections) > 0:
                self.pos_x = max([surr[1] for surr in intersections])
            else:
                obj.set_position(self.pos_x - obj.width, self.pos_y_min)
                break

        self.last_obj = obj

    def add_obj(self, obj: ReaderObj):
        '''
        Добавляет объект на страницу.
        '''
        if isinstance(obj, Word) or isinstance(obj, Image) and obj.layout == 'embedded':
            # Если объект - слово или встроенное изображение, то:
            # 1. Если это не начало фрагмента, то необходимо поставить пробел.
            # Если при постановке пробела, мы пересекаемся с окруженными изображениями,
            # то перемещаем курсор вправо до конца пересечения.
            # Иначе устанавливаем пробел.
            # 2. Устанавливаем объект на странице.
            # 3. Устанавливаем максимальную координату y текущей строки.
            # 4. Устанавливаем, что это не начало фрагмента.
            if not self.is_start_of_fragment:
                intersections = list(
                    filter(
                        lambda surr:
                            surr[0] - 1 in range(self.pos_x, self.pos_x + self.char_width)
                            and self.pos_y_min < surr[2],
                        self.surroundeds
                    )
                )

                if len(intersections) > 0:
                    self.pos_x = max([surr[1] for surr in intersections])
                else:
                    self.space()

            self.set_object(obj)

            self.pos_y_max = max(self.pos_y_max, self.pos_y_min + obj.height)

            self.is_start_of_fragment = False
        elif isinstance(obj, Image) and obj.layout == 'surrounded':
            # Если объект - окруженное изображение, то:
            # 1. Устанавливаем объект на странице в свободном месте.
            # 2. Устанавливаем, что это начало фрагмента.
            # 3. Добавляем объект в список окруженных изображений.
            self.set_object(obj)
            self.is_start_of_fragment = True
            self.surroundeds.append(
                (self.pos_x - obj.width, self.pos_x, self.pos_y_min + obj.height)
            )
        elif isinstance(obj, Image) and obj.layout == 'floating':
            #Если объект - плавающее изображение, то:
            # 1. Берём последний объект и находим его координату x конца.
            # Если картинка выходит за правую границу,
            # то устанавливаем её вправо от последнего объекта.
            # Если картинка выходит за левую границу,
            # то устанавливаем её влево от последнего объекта.
            # Иначе Устанавливаем объект на странице.
            # 2. Устанавливаем, позицию последнего объекта.
            # 3. Устанавливаем, что это последний объект.
            last_obj = self.last_obj
            last_obj_pos_x_end = last_obj.pos_x + last_obj.width

            if last_obj_pos_x_end + obj.width + obj.dx > self.page_width:
                image_pos_x = w - obj.width
            elif last_obj_pos_x_end + obj.dx < 0:
                image_pos_x = 0
            else:
                image_pos_x = last_obj_pos_x_end + obj.dx
            image_pos_y = last_obj.pos_y + obj.dy

            obj.set_position(image_pos_x, image_pos_y)

            self.last_obj = obj

        # Удаляем окруженные изображения, которые
        # ниже минимальной координаты y текущей строки.
        self.surroundeds = list(
            filter(
                lambda x: x[2] > self.pos_y_min, self.surroundeds
            )
        )


# Входные данные:
with open('input.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Обработка входных данных:
w, h, c = map(int, lines[0].split())
lines = lines[1:]

# Алгоритм:
reader = Reader(w, c, h)

CURRENT_IMAGE = None

for line in lines:
    words = line.split()
    if len(words) == 0:
        reader.paragraph()
    for word in words:
        if not CURRENT_IMAGE:
            if word == '(image':
                CURRENT_IMAGE = Image()
                continue
            else:
                new_obj = Word(word)
                reader.add_obj(new_obj)
        else:
            if word[-1] != ')':
                CURRENT_IMAGE.set_param_from_str(word)
                continue
            else:
                CURRENT_IMAGE.set_param_from_str(word[:-1])
                reader.add_obj(CURRENT_IMAGE)

                print(f"{reader.last_obj.pos_x} {reader.last_obj.pos_y}")

                CURRENT_IMAGE = None
