from random import randint
from GamePole import GamePole 
from Ship import Ship   
    
def main():
    SIZE_GAME_POLE = 10

    pole = GamePole(SIZE_GAME_POLE)
    pole.init()
    pole.show()

    pole.move_ships()
    print()
    pole.show()
    pole = GamePole(SIZE_GAME_POLE)
    ship = Ship(3)

    # x_1 = 3
    # y_1 = 2
    # x_2 = 6
    # y_2 = 6
    # x_3 = 5
    # y_3 = 6
    # x_4 = 7
    # y_4 = 2

    # print(ship._is_intersect_rect(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4))

    # x_1 = 1
    # y_1 = 6
    # x_2 = 3
    # y_2 = 0
    # x_3 = 2
    # y_3 = 4
    # x_4 = 6
    # y_4 = 3


    # print(ship._is_intersect_rect(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4))

    # x_1 = 3
    # y_1 = 8
    # x_2 = 6
    # y_2 = 8
    # x_3 = 5
    # y_3 = 2
    # x_4 = 7
    # y_4 = 2

    # print(ship._is_intersect_rect(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4))
    
if __name__ == "__main__":
    main()
