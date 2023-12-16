from random import randint, choice
from copy import copy
from Ship import Ship

class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = None
        self._pole = [[0] * size for i in range(size)]
        # self._pole = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
    def init(self):
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))
                      ]
        
        self._place_ships()
        
    def get_ships(self):
        # return tuple(tuple(row for row in self._ships))
        
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
 