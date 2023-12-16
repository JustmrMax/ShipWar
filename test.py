from random import randint, choice
from copy import copy
from Ship import Ship

class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = None
        self._pole = [[0] * size for i in range(size)]
        
    def init(self):
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))
                      ]
        
        self._place_ships()
        
    def get_ships(self):
        return self._ships
    
    def _check_collisions(self, ship, go): 
        got_hit = False      
        self._potential_ship = copy(ship)
        self._potential_ship.move(go)

        got_hit |= self._potential_ship.is_out_pole(self._size)

        if (got_hit):
            return True
            
        for i_ship in self._ships:
            if (ship.id == i_ship.id):
                continue

            got_hit |= self._potential_ship.is_collide(i_ship)
                
            if got_hit:
                break
        
        return got_hit
      
    def _place_ships(self):
        for i, ship in enumerate(self._ships):
            got_hit = True
            length = ship.get_length()
            tp = ship.get_tp()

            while(got_hit):
                got_hit = False
                x = randint(0, self._size - 1)
                y = randint(0, self._size - 1)

                if (tp == 1):
                    x -= length
                else:
                    y -= length

                if (x < 0 or y < 0):
                    got_hit = True
                    continue

                ship.set_start_coords(x, y)

                for i_ship in self._ships:
                    if (ship.id == i_ship.id):
                        continue

                    got_hit = ship.is_collide(i_ship)

                    if (got_hit):
                        break

            self._ships[i] = ship
            self._init_pole()

    def move_ships(self):
        for i, ship in enumerate(self._ships):
            got_hit = False
            go = choice([-1, 1])
            
            got_hit |= self._check_collisions(ship, go)
            
            if (got_hit):
                go = -1 if go == 1 else 1
                got_hit |= self._check_collisions(ship, go)

            if (not got_hit):
                self._ships[i] = self._potential_ship
                self._init_pole()
        else:
            return False      
                
    def _clear_pole(self):
        for i in range(self._size):
            for j in range(self._size):
                self._pole[i][j] = 0          
    
    def _init_pole(self):
        self._clear_pole()

        for ship in self._ships:
            x_offset = 0
            y_offset = 0
            x, y = ship.get_start_coords()
            length = ship.get_length()
            tp = ship.get_tp()

            if x is None or y is None:
                continue

            for i in range(length):
                if (tp == 1):
                    self._pole[y][x + x_offset] = 1
                    x_offset += 1
                else:
                    self._pole[y + y_offset][x] = 1
                    y_offset += 1
    
    def show(self):
        self._init_pole()
        
        for i in range(self._size):
            for j in range(self._size):
                print(self._pole[i][j], end=" ")
            
            print()
            
    def get_pole(self):
        return tuple(tuple(row) for row in self._pole)

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

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

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
    

def main():
    ship = Ship(2)
    ship = Ship(2, 1)
    ship = Ship(3, 2, 0, 0)

    assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
    assert ship._cells == [1, 1, 1], "неверный список _cells"
    assert ship._is_move, "неверное значение атрибута _is_move"

    ship.set_start_coords(1, 2)
    assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
    assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"

    ship.move(1)
    s1 = Ship(4, 1, 0, 0)
    s2 = Ship(3, 2, 0, 0)
    s3 = Ship(3, 2, 0, 2)

    assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
    assert s1.is_collide(s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"

    s2 = Ship(3, 2, 1, 1)
    assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"

    s2 = Ship(3, 1, 8, 1)
    assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"

    s2 = Ship(3, 2, 1, 5)
    assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"

    s2[0] = 2
    assert s2[0] == 2, "неверно работает обращение ship[indx]"

    p = GamePole(10)
    p.init()
    for nn in range(5):
        for s in p._ships:
            assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"

            for ship in p.get_ships():
                if s != ship:
                    assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
        p.move_ships()
        
    gp = p.get_pole()
    assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
    assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"

    pole_size_8 = GamePole(8)
    pole_size_8.init()


if __name__ == "__main__":
    main()