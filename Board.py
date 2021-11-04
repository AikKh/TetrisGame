import time
import pygame
import sys
from Block import Block

class Board:

    black = (0, 0, 0)
    touch_block = False
    surface = None

    width = 560
    height = 800

    obj_blocks_list = []

    game_over = False
    game_restart = False
    pause = False

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
#eeeee
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

    def surfacePurifier(self):
        self.surface.fill((0, 0, 0))
        self.obj_blocks_list = []

    def restart(self):
        my_font = pygame.font.SysFont('times new roman', 49)
        game_over_surface = my_font.render('Game over', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect()
        game_over2_surface = my_font.render('Press Space or Q', True, (255, 255, 255))
        game_over2_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.width/2, self.width/4)
        game_over2_rect.midtop = (self.width/2 - 80, self.width/4 + 60)
        self.surface.fill(self.black)
        self.surface.blit(game_over_surface, game_over_rect)
        self.surface.blit(game_over2_surface, game_over2_rect)
        pygame.display.flip()

    def pauseFunction(self, stage):
        if stage == 1:
            my_font = pygame.font.SysFont('times new roman', 49)
            pause_surface = my_font.render('Paused', True, (255, 255, 255))
            pause_rect = pause_surface.get_rect()
            pause_rect.midtop = (self.width/2, self.width/4)
            self.surface.blit(pause_surface, pause_rect)
            pygame.display.flip()
        elif stage == 2:
            self.surface.fill(self.black)
            self.allBlocksDraw()
            self.pause = False
        


    def allBlocksDraw(self):
        for block in self.obj_blocks_list:
            for x, y in block._cors:
                pygame.draw.rect(self.surface, block.color, [x  * 40, y * 40, 39, 39])

    def main(self):

        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill(self.black)
        pygame.display.set_caption("Tetris game")

        fps = 14
        clock = pygame.time.Clock()
        frame_count = 0


        while not self.game_over:


            while self.game_restart:
                self.restart()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.surfacePurifier()
                            self.game_restart = False
                        elif event.key == pygame.K_q:
                            self.game_restart = False
                            self.game_over = True

            lines = self.linesToRemove()

            self.allBlocksMoveDown(lines)

            for block in self.obj_blocks_list:
                for cor in block._cors:
                    if cor[1] < 0:
                        self.game_restart = True
                        continue

            self.touch_block = False

            new_block = Block(7, -1)
            new_block.blockMaker(new_block.x, new_block.y)
            direction = 2


            while not self.touch_block:

                while self.pause:
                    self.pauseFunction(1)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                self.pauseFunction(2)

                pygame.display.flip()
                clock.tick(fps) 

                if new_block.cantMove() or new_block.touchBlock(self.obj_blocks_list):
            
                    self.allBlocksDraw()
                    self.obj_blocks_list.append(new_block)
                    self.touch_block = True
                    continue


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            new_block.cutBlocks(self.surface)
                            new_block.changeState(self.obj_blocks_list)
                            new_block.drawBlocks(self.surface)
                        elif event.key == pygame.K_p:
                            self.pause = True

                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if new_block.nearBlockTouch(self.obj_blocks_list, -1):
                            pass
                        else:
                            new_block.move(self.surface, 3)
                    elif event.key == pygame.K_RIGHT:
                        if new_block.nearBlockTouch(self.obj_blocks_list, 1):
                            pass
                        else:
                            new_block.move(self.surface, 1)
                    elif event.key == pygame.K_DOWN:
                        new_block.move(self.surface, 2)

                if new_block.cantMove() or new_block.touchBlock(self.obj_blocks_list):
        
                    self.allBlocksDraw()
                    self.obj_blocks_list.append(new_block)
                    self.touch_block = True
                    continue

                
                frame_count += 1
                if frame_count == 5:
                    new_block.move(self.surface, direction)
                    frame_count = 0
                

game = Board()
game.main()
