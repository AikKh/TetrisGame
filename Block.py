import pygame
import random

class Block():

    
    colors_list = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 128, 0), (255, 0, 127), (51, 255, 255), (153, 51, 255)]


    def __init__(self, x, y):
        self.shape = random.randrange(7)
        self._cors = []
        self.x = x
        self.y = y
        self.color = self.colors_list[random.randrange(7)]
        self.state = 0


    def blockMaker(self, x, y):
        shape0 = [[(x, y), (x - 1, y), (x, y - 1), (x, y - 2)],
                  [(x, y), (x, y - 1), (x + 1, y), (x + 2, y)],
                  [(x, y), (x + 1, y), (x, y + 1), (x, y + 2)],
                  [(x, y), (x - 1, y), (x - 2, y), (x, y + 1)]]

        shape1 = [[(x, y), (x, y - 1), (x, y - 2), (x, y - 3)],
                  [(x, y), (x - 1, y), (x + 1, y), (x + 2, y)],
                  [(x, y), (x, y - 1), (x, y - 2), (x, y - 3)],
                  [(x, y), (x - 1, y), (x + 1, y), (x + 2, y)]]

        shape2 = [[(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)],
                  [(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)],
                  [(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)],
                  [(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)]]

        shape3 = [[(x, y), (x + 1, y), (x, y - 1), (x - 1, y - 1)],
                  [(x, y), (x + 1, y - 1), (x + 1, y), (x, y + 1)],
                  [(x, y), (x + 1, y), (x, y - 1), (x - 1, y - 1)],
                  [(x, y), (x + 1, y - 1), (x + 1, y), (x, y + 1)]]

        shape4 = [[(x, y), (x + 1, y), (x, y - 1), (x - 1, y)],
                  [(x, y), (x, y - 1), (x + 1, y), (x, y + 1)],
                  [(x, y), (x + 1, y), (x, y + 1), (x - 1, y)],
                  [(x, y), (x, y - 1), (x - 1, y), (x, y + 1)]]

        shape5 = [[(x, y), (x + 1, y), (x, y - 1), (x, y - 2)],
                  [(x, y), (x, y + 1), (x + 1, y), (x + 2, y)],
                  [(x, y), (x - 1, y), (x, y + 1), (x, y + 2)],
                  [(x, y), (x - 1, y), (x - 2, y), (x, y - 1)]]

        shape6 = [[(x, y), (x - 1, y), (x, y - 1), (x + 1, y - 1)],
                  [(x, y), (x + 1, y + 1), (x + 1, y), (x, y - 1)],
                  [(x, y), (x - 1, y), (x, y - 1), (x + 1, y - 1)],
                  [(x, y), (x + 1, y + 1), (x + 1, y), (x, y - 1)]]


        shape_list = [shape0, shape1, shape2, shape3, shape4, shape5, shape6]

        for co in range(4):
            self._cors.append(shape_list[self.shape][self.state % 4][co])

        return self._cors


    def moveCors(self, dir):
        if self.x == -1 or self.x == 14:
            return 
        elif dir == 1:
            for x, y in self._cors:
                if x + 1 >= 14:
                    return False
            for co in range(len(self._cors)):
                self._cors[co] = (self._cors[co][0] + 1, self._cors[co][1])
        elif dir == 2:
            for co in range(len(self._cors)):
                self._cors[co] = (self._cors[co][0], self._cors[co][1] + 1)
        elif dir == 3:
            for x, y in self._cors:
                if x - 1 <= -1:
                    return False
            for co in range(4):
                self._cors[co] = (self._cors[co][0] - 1, self._cors[co][1])


    def cutBlocks(self, surface):
        for x, y in self._cors:
            pygame.draw.rect(surface, (0, 0, 0), [x  * 40, y * 40, 40, 40])

    def drawBlocks(self, surface):
        for x, y in self._cors:
            pygame.draw.rect(surface, self.color, [x  * 40, y * 40, 39, 39])

    def cantMove(self):
        for x, y in self._cors:
            if y + 1 == 20:
                return True

    def nearBlockTouch(self, obj_blocks_list, i):
        for block in obj_blocks_list:
            for cor in block._cors: 
                for new_cor in self._cors:
                    if cor == (new_cor[0] + i, new_cor[1] + 1) or cor == (new_cor[0] + i, new_cor[1] - 1):
                        return True

    def touchBlock(self, obj_blocks_list):
        for block in obj_blocks_list:
            for cor in block._cors:
                for new_cor in self._cors:
                    if cor == (new_cor[0], new_cor[1] + 1):
                        return True

    def getCutCors(self):
        check_list = []
        for i in range(14):
            check_list.append((i, self.y))
        return check_list

    def setColorToCor(self, cor):
        pass

    def changeState(self, obj_blocks_list):
        if self.nearBlockTouch(obj_blocks_list, -1) or self.nearBlockTouch(obj_blocks_list, 1) or self.y > 17:
            return False
        x = self._cors[0][0]
        y =  self._cors[0][1]
        self.x = x
        self.y = y
        self._cors.clear()
        self.state += 1
        new_cors = self.blockMaker(self.x, self.y)
        for co_x, co_y in new_cors:
            if co_x >= 14 or co_x <= -1:
                self.state -= 1
                self._cors.clear()
                new_cors = self.blockMaker(self.x, self.y)
        return True
    

    def move(self, display, dir):
        self.cutBlocks(display)
        self.moveCors(dir)
        self.drawBlocks(display)
