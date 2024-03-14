with open('input.txt', 'r') as file:
    lines = file.readlines()

w, h, c = map(int, lines[0].split())
lines = lines[1:]

class Image:
    pos_x = 0
    pos_y = 0

    def __init__(self, layout="embeded", width=0, height=0, dx=0, dy=0):
        self.layout = layout
        self.width = width
        self.height = height
        self.dx = dx
        self.dy = dy

    def set_param_from_str(self, string: str):
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

    def set_position(self, x: int, y: int):
        self.pos_x = x
        self.pos_y = y

    def __str__(self):
        string = f'Image: layout={self.layout} width={self.width} height={self.height}'
        if self.layout == 'floating':
            return string + f' dx={self.dx} dy={self.dy}'
        else:
            return string

pos_x_start = 0
pos_x_end = 0
pos_y_min = 0
pos_y_max = h
CURRENT_IMAGE = None
IS_IMAGE = False
LAST_IMAGE = None
LAST_V_IMAGE = None
surrounded = []


for line in lines:
    words = line.strip().split()
    if len(words) == 0 or words[0] == '':
        pos_x_start = 0
        pos_x_end = 0
        if len(surrounded) > 0:
            pos_y_min = max(pos_y_max, *[y for _, _, y in surrounded])
        else:
            pos_y_min = pos_y_max
        pos_y_max = pos_y_min + h
        LAST_IMAGE = None
        LAST_V_IMAGE = None
        #print("АБЗАЦ")
        #print(f'\tpos_y: {pos_y_min} {pos_y_max}')
    for word in words:
        if not IS_IMAGE:
            if word == '(image':
                IS_IMAGE = True
                CURRENT_IMAGE = Image()
                continue
            else:
                #print(word, end=' ')
                if LAST_V_IMAGE is None or LAST_V_IMAGE.layout == 'embedded':
                    intersections = list(
                        filter(
                            lambda surr:
                                (surr[0] - 1 in range(pos_x_end - c, pos_x_end)
                                and pos_y_min < surr[2]),
                            surrounded
                        )
                    )
                    if len(intersections) > 0:
                        pos_x_end = max([surr[1] for surr in intersections])

                word_length = len(word) * c

                if pos_x_end + word_length > w:
                    pos_x_start = 0
                    pos_x_end = word_length
                    pos_y_min = pos_y_max
                    pos_y_max += h
                else:
                    pos_x_start = pos_x_end
                    pos_x_end += word_length

                IS_NO_SET = True
                while IS_NO_SET:
                    intersections = list(
                        filter(
                            lambda surr:
                                (pos_x_end - 1 in range(surr[0], surr[1])
                                or surr[1] - 1 in range(pos_x_start, pos_x_end))
                                and pos_y_min < surr[2],
                            surrounded)
                        )
                    print(intersections)

                    if len(intersections) > 0:
                        pos_x_start = max([surr[1] for surr in intersections])
                        pos_x_end = pos_x_start + word_length
                    else:
                        IS_NO_SET = False

                    if pos_x_end > w:
                        pos_x_start = 0
                        pos_x_end = word_length
                        pos_y_min = pos_y_max
                        pos_y_max += h

                pos_x_end += c
  
                LAST_IMAGE = None
                LAST_V_IMAGE = None
        else:
            if word[-1] != ')':
                CURRENT_IMAGE.set_param_from_str(word)
                continue
            else:
                CURRENT_IMAGE.set_param_from_str(word[:-1])
                print(CURRENT_IMAGE)

                if CURRENT_IMAGE.layout == 'embedded':

                    if LAST_V_IMAGE is None or LAST_V_IMAGE.layout == 'embedded':
                        intersections = list(
                            filter(
                                lambda surr:
                                    (surr[0] - 1 in range(pos_x_end - c, pos_x_end)
                                    and pos_y_min < surr[2]),
                                surrounded
                            )
                        )
                        if len(intersections) > 0:
                            pos_x_end = max([surr[1] for surr in intersections])

                    if pos_x_end + CURRENT_IMAGE.width > w:
                        pos_x_start = 0
                        pos_x_end = CURRENT_IMAGE.width
                        pos_y_min = pos_y_max
                        pos_y_max += h
                    else:
                        pos_x_start = pos_x_end
                        pos_x_end += CURRENT_IMAGE.width

                    IS_NO_SET = True
                    while IS_NO_SET:
                        intersections = list(
                            filter(
                                lambda surr:
                                    (pos_x_end - 1 in range(surr[0], surr[1])
                                    or surr[1] - 1 in range(pos_x_start, pos_x_end))
                                    and pos_y_min < surr[2],
                                surrounded)
                            )

                        if len(intersections) > 0:
                            pos_x_start = max([surr[1] for surr in intersections])
                            pos_x_end = pos_x_start + CURRENT_IMAGE.width
                        else:
                            IS_NO_SET = False

                        if pos_x_end > w:
                            pos_x_start = 0
                            pos_x_end = CURRENT_IMAGE.width
                            pos_y_min = pos_y_max
                            pos_y_max += h
                    pos_y_max = max(pos_y_max, pos_y_min + CURRENT_IMAGE.height)
                    pos_x_end += c
                    CURRENT_IMAGE.set_position(pos_x_start, pos_y_min)
                elif CURRENT_IMAGE.layout == 'surrounded':
                    if pos_x_end != 0 and (LAST_V_IMAGE is None or LAST_V_IMAGE.layout == 'embedded'):
                        pos_x_end -= c

                    if pos_x_end + CURRENT_IMAGE.width > w:
                        pos_x_start = 0
                        pos_x_end = CURRENT_IMAGE.width
                        pos_y_min = pos_y_max
                        pos_y_max += h
                    else:
                        pos_x_start = pos_x_end
                        pos_x_end += CURRENT_IMAGE.width

                    IS_NO_SET = True
                    while IS_NO_SET:
                        intersections = list(
                            filter(
                                lambda surr:
                                    (pos_x_end - 1 in range(surr[0], surr[1])
                                    or surr[1] - 1 in range(pos_x_start, pos_x_end))
                                    and pos_y_min < surr[2],
                                surrounded)
                            )
                        #print(intersections)

                        if len(intersections) > 0:
                            pos_x_start = max([surr[1] for surr in intersections])
                            pos_x_end = pos_x_start + CURRENT_IMAGE.width
                        else:
                            IS_NO_SET = False

                        if pos_x_end > w:
                            pos_x_start = 0
                            pos_x_end = CURRENT_IMAGE.width
                            pos_y_min = pos_y_max
                            pos_y_max += h
                    
                    surrounded.append((pos_x_start, pos_x_end, pos_y_min + CURRENT_IMAGE.height))
                    CURRENT_IMAGE.set_position(pos_x_start, pos_y_min)
                elif CURRENT_IMAGE.layout == 'floating':
                    if pos_x_end != 0 and (LAST_IMAGE is None or LAST_IMAGE.layout == 'embedded'):
                        pos_x_end -= c

                    if LAST_IMAGE is None or LAST_IMAGE.layout != 'floating':
                        if pos_x_end + CURRENT_IMAGE.dx + CURRENT_IMAGE.width > w:
                            image_pos_x = w - CURRENT_IMAGE.width
                        elif pos_x_end + CURRENT_IMAGE.dx < 0:
                            image_pos_x = 0
                        else:
                            image_pos_x = pos_x_end + CURRENT_IMAGE.dx
                        CURRENT_IMAGE.set_position(image_pos_x, pos_y_min + CURRENT_IMAGE.dy)
                    else:
                        if LAST_IMAGE.pos_x + CURRENT_IMAGE.dx + CURRENT_IMAGE.width > w:
                            image_pos_x = w - CURRENT_IMAGE.width
                        elif LAST_IMAGE.pos_x + CURRENT_IMAGE.dx < 0:
                            image_pos_x = 0
                        else:
                            image_pos_x = LAST_IMAGE.pos_x + LAST_IMAGE.width + CURRENT_IMAGE.dx
                        CURRENT_IMAGE.set_position(image_pos_x, LAST_IMAGE.pos_y + CURRENT_IMAGE.dy)

                    if pos_x_end != 0 and (LAST_IMAGE is None or LAST_IMAGE.layout == 'embedded'):
                        pos_x_end += c

                print(f"{CURRENT_IMAGE.pos_x} {CURRENT_IMAGE.pos_y}")
                IS_IMAGE = False
                LAST_IMAGE = CURRENT_IMAGE
                if CURRENT_IMAGE.layout != 'floating':
                    LAST_V_IMAGE = CURRENT_IMAGE
                CURRENT_IMAGE = None

        surrounded = list(filter(lambda x: x[2] > pos_y_min, surrounded))
        print(f"\tpos_x: {pos_x_start} {pos_x_end} pos_y: {pos_y_min} {pos_y_max}")
