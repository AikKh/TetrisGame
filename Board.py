import time
import pygame
import sys
from Block import Block

class Board:

    black = (0, 0, 0)
    touch_block = False
    surface = None

    obj_blocks_list = []

    game_over = False

    def fullLineCheck(self):
    
        range_14 = list(range(14))

        minY = 19
        maxY = 20
        for block in self.obj_blocks_list:
            for cor in block._cors:
                if cor[1] < minY:
                    minY = cor[1]

        if minY < 0:
            minY = 0

        full_liens = []

        for i in range(minY, maxY):
            x_array = []
            for block in self.obj_blocks_list:
                for cor in block._cors:
                    if cor[1] == i:
                        x_array.append(cor[0])

            x_array = list(set(x_array))
            if x_array == range_14:
                full_liens.append(i)

        return full_liens

    def linesToRemove(self):

        lines = self.fullLineCheck()
        cut_list = []

        for line in lines:
            for block in self.obj_blocks_list:
                for x, y in block._cors:
                    if line == y:
                        pygame.draw.rect(self.surface, (0, 0, 0), [x  * 40, y * 40, 40, 40])
                        cut_list.append((x, y))

        for cut_cor in cut_list:
            for block in self.obj_blocks_list:
                    for cors in block._cors:
                        if cut_cor == cors:
                            block._cors.remove(cut_cor)

        return lines

    def allBlocksMoveDown(self, lines):
        if lines != []:
            for block in self.obj_blocks_list:
                for x, y in block._cors:
                    if y < lines[0]:
                        for i in range(len(lines)):
                            block.move(self.surface, 2)
                        break

    def main(self):

        pygame.init()
        self.surface = pygame.display.set_mode((560, 800))
        self.surface.fill(self.black)
        pygame.display.set_caption("Tetris game")

        fps = 7
        clock = pygame.time.Clock()

        
        while not self.game_over:

            lines = self.linesToRemove()

            self.allBlocksMoveDown(lines)

            for block in self.obj_blocks_list:
                for cor in block._cors:
                    if cor[1] < 0:
                        self.game_over = True

            self.touch_block = False

            new_block = Block(7, -1)
            new_block.blockMaker(new_block.x, new_block.y)
            direction = 2


            while not self.touch_block:


                if new_block.cantMove() or new_block.touchBlock(self.obj_blocks_list):
                      
                    self.obj_blocks_list.append(new_block)
                    self.touch_block = True
                    continue


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if new_block.nearBlockTouch(self.obj_blocks_list, -1):
                                continue
                            new_block.move(self.surface, 3)
                        elif event.key == pygame.K_RIGHT:
                            if new_block.nearBlockTouch(self.obj_blocks_list, 1):
                                continue
                            new_block.move(self.surface, 1)
                        elif event.key == pygame.K_SPACE:
                            new_block.cutBlocks(self.surface)
                            if not new_block.changeState(self.obj_blocks_list):
                                new_block.drawBlocks(self.surface)


                new_block.move(self.surface, direction)
                pygame.display.flip()
                clock.tick(fps) 

game = Board()
game.main()
