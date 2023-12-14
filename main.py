from random import randint

class Ship:
    def __init__(self, length, tp = 1, x = None, y = None):
        self._x = x
        self._y = y
        self._length = length
        self._tp = tp
        self._is_move = True
        self._cells = [[1] * length]
    
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
        if (go > 0):
            if (self._tp == 1):
                self.x += 1
            else:
                self.y -= 1
        else:
            if (self._tp == 1):
                self.x -= 1
            else:
                self.y += 1
                
    def is_collide(self, ship):
        # Проверка пересечения двух массивов, представленных как прямоуголиники
        x_ship_1, y_ship_1 = ship.get_start_coords()
        length_ship = ship.get_length()
        tp_ship = ship.get_tp()
        
        if x_ship_1 != 0:
            x_ship_1 -= 1
        if y_ship_1 != 0:
            y_ship_1 -= 1
            
        if (tp_ship == 1):
            x_ship_2 = x_ship_1 + length_ship
        else:
            x_ship_2 = x_ship_1 + 1
            
        if (tp_ship == 2):
            y_ship_2 = y_ship_1 + length_ship
        else:
            y_ship_2 = y_ship_1 + 1
            
        x_1, y_1 = self.get_start_coords()
        tp = self.get_tp()
        length = self.get_length()
        
        if (tp == 1):
            x_2 = x_1 + length - 1
        else:
            x_2 = x_1
            
        if (tp == 2):
            y_2 = y_1 + length - 1
        else:
            y_2 = y_1
        
        if (y_ship_1 < y_2 or y_ship_2 > y_1 or x_ship_2 < x_1 or x_ship_1 > x_2):
            return True
        else:
            return False

    def is_out_pole(self, size):
        if self._x >= size:
            return True
        elif self._y >= size:
            return True
        elif self._x < 0:
            return True
        elif self._y < 0:
            return True
        else:
            return False
        
    def __getitem__(self, *args):
        return self._cells[args[0]]
    
    def __setitem__(self, *args):
        self._cells[args[0]] = args[1]
        
    def get_length(self):
        return self._length
    
    def get_tp(self):
        return self._tp
        
class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = None
        self._pole = [[0] * size] * size
        
    def init(self):
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))
                      ]
        
        self._place_ships()
        
    def get_ships(self):
        return self._ships
    
    def _check_collisions(self, ship, tp): 
        got_hit = False      
        x, y = ship.get_start_coords()
        next_x = 0
        next_y = 0
        length = ship.get_length()
        tp = ship.get_tp()
        go = randint(1, 2)
            
        if (tp == 1):
            if (go > 0):
                next_x = x + 1 
            else:
                next_x = x - 1
                
            next_y = y
                
        else:
            if (go > 0):
                next_y = y - 1
            else:
                next_y = y + 1
                    
            next_x = x
                
        self._potential_ship = Ship(length, tp, next_x, next_y)
            
        got_hit &= self._potential_ship.is_out_pole(self._size)
            
        for i_ship in self._ships:
            got_hit &= self._potential_ship.is_collide(i_ship)
                
            if not got_hit:
                break
        
        return got_hit
      
    def _place_ships(self):
        for i, ship in enumerate(self._ships):
            is_placed = False
            while(not is_placed):
                x = randint(0, self._size)
                y = randint(0, self._size)

                ship.set_start_coords(x, y)
                is_placed = not self._check_collisions(ship, ship.get_tp())              
            
            self._ships[i] = ship


    def move_ships(self):
        # potential_ship = None
        got_hit = False
        
        for i, ship in enumerate(self._ships):
            tp = randint(1, 2)
            
            got_hit &= self._check_collisions(ship, tp)
            
            if (not got_hit):
                tp = 1 if tp == 2 else 2
                got_hit &= self._check_collisions(ship, tp)

            if (not got_hit):
                self._ships[i] = self._potential_ship
            else:
                return False      
                
                
    
    def _init_pole(self):
        for ship in self._ships:
            x_offset = 0
            y_offset = 0
            x, y = ship.get_start_coords()
            length = ship.get_length()
            tp = ship.get_tp()
            
            for i in range(length):
                if (tp == 1):
                    self._pole[x + x_offset][y] = 1
                    x_offset += 1
                else:
                    self._pole[x][y + y_offset] = 1
                    y_offset += 1
    
    def show(self):
        self._init_pole()
        
        for i in range(self.size):
            for j in range(self.size):
                print(self._pole[i][j])
                
            print("\n")
            
    def get_pole(self):
        return self._pole
    
    
    
def main():
    SIZE_GAME_POLE = 10

    pole = GamePole(SIZE_GAME_POLE)
    pole.init()
    pole.show()

    pole.move_ships()
    print()
    pole.show()
    
if __name__ == "__main__":
    main()
