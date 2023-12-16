from random import randint

class Ship:
    ID = 0

    def __new__(cls, *args, **kwargs):
        cls.ID += 1
        
        return super().__new__(cls)


    def __init__(self, length, tp = 1, x = None, y = None):
        self._x = x
        self._y = y
        self._length = length
        self._tp = tp
        self._is_move = True
        self._cells = [1] * length
        self.id = self.ID
    
    #def _init_cells(self):
    #   for i in range(length):
    #      for j in range(length):
    #         self.


    def set_start_coords(self, x, y):
        self._x = x
        self._y = y
        # self._next_x = None
        # self._next_y = None


    def get_start_coords(self):
        return (self._x, self._y)
    

    def move(self, go):
        if (not self._is_move):
            return False

        if (go > 0):
            if (self._tp == 1):
                self._x += 1
            else:
                self._y += 1
        else:
            if (self._tp == 1):
                self._x -= 1
            else:
                self._y -= 1


    def is_collide(self, ship):
        # Проверка пересечения двух массивов, представленных как прямоуголиники
        tp_1 = self.get_tp()
        tp_2 = ship.get_tp()
        length_1 = self.get_length()
        length_2 = ship.get_length()

        # Получаем координаты первого прямоугольника
        x_1, y_1 = self.get_start_coords()

        if x_1 is None or y_1 is None:
            return False
        
        if (tp_1 == 1):
            x_2 = x_1 + length_1 - 1
            y_2 = y_1
        else:
            y_2 = y_1 + length_1 - 1
            x_2 = x_1

        # Получаем координаты второго прямоугольника
        x_3, y_3 = ship.get_start_coords()

        if x_3 is None or y_3 is None:
            return False

        if (tp_2 == 1):
            x_4 = x_3 + length_2 - 1
            y_4 = y_3
        else:
            y_4 = y_3 + length_2 - 1
            x_4 = x_3

        # Коректируем координаты первого прямоугольника (расширяем его во всех напрявлениях на 1)
        if x_1 > 0:
            x_1 -= 1
        if y_1 > 0:
            y_1 -= 1

        x_2 += 1
        y_2 += 1
        
        return self._is_intersect_rect(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4)


    def _is_intersect_rect(self, x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4):
        # if (x_1 < x_4 and x_2 > x_3 and y_1 > y_4 and y_2 < y_3):
        #     return True
        # else:
        #     return False 
        # return not(x_4 > x_2 or x_4 < x_1 or y_3 > y_2 or y_4 < y_1)
        # if (x_3 in [x_1, x_2 + 1] and y_3 in [y_1, y_2 + 1] or x_4 in [x_1, x_2 + 1] and y_4 in [y_2, y_1 + 1]):
        #     return True
        # else:
        #     return False
        
        if (x_1 < x_2):
            x_range = [i for i in range(x_1, x_2 + 1)]
        else:
            x_range = [i for i in range(x_2, x_1 + 1)]

        if (y_1 < y_2):
            y_range = [i for i in range(y_1, y_2 + 1)]
        else:
            y_range = [i for i in range(y_2, y_1 + 1)]

        if (x_3 in x_range and y_3 in y_range or x_4 in x_range and y_4 in y_range):
            return True
        else:
            return False


    def is_out_pole(self, size):
        if self._x >= size or self._y >= size or self._x < 0 or self._y < 0:
            return True

        if (self.get_tp() == 1):
            if (self._x + self.get_length() >= size):
                return True
        else:
            if (self._y + self.get_length() >= size):
                return True

        return False
        
    def __getitem__(self, *args):
        return self._cells[args[0]]
    

    def __setitem__(self, *args):
        self._cells[args[0]] = args[1]


    def get_length(self):
        return self._length
    

    def get_tp(self):
        return self._tp