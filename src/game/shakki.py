import pygame
import os
from entities.bishop import Bishop
from entities.king import King
from entities.queen import Queen
from entities.knight import Knight
from entities.pawn import Pawn
from entities.rook import Rook

dirname = os.path.dirname(__file__)

class Shakki:
    def init(self):
        pygame.init()

        self.lauta = [[0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0]]
        
        self.load_tiles()
        
        self.height_and_width = len(self.lauta)
        self.scale = self.tiles[0].get_width() 
        win_height_and_width = self.height_and_width * self.scale
        self.screen = pygame.display.set_mode((win_height_and_width, win_height_and_width))
        self.black_pieces = pygame.sprite.Group()
        self.white_pieces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        

        self.chosen_piece = []
        self.chosen_piece_original_position = None
        self.white_to_move = True

        self.draw_board()
        self.set_board()

        pygame.display.set_caption("shakki")

        self.main_loop()
    
    def load_tiles(self):
        self.tiles = []
        for name in ["sqrw","sqrb"]:
            self.tiles.append(pygame.image.load(
                os.path.join(dirname,"..","assets",name+".png")
            ))        

    def set_board(self):
        for x in range(len(self.lauta)):
            for y in range(len(self.lauta)):
                scaled_x = x * self.scale
                scaled_y = y * self.scale
                if y == 0:
                    if x == 0 or x == 7:
                        self.black_pieces.add(Rook(scaled_x,scaled_y, "rook", "b")) 
                    if x == 1 or x == 6:
                        self.black_pieces.add(Knight(scaled_x,scaled_y, "knight", "b")) 
                    if x == 2 or x == 5:
                        self.black_pieces.add(Bishop(scaled_x,scaled_y, "bishop", "b"))
                    if x == 3:
                        self.black_pieces.add(Queen(scaled_x,scaled_y, "queen", "b"))
                    if x == 4:
                        self.black_pieces.add(King(scaled_x,scaled_y, "king", "b"))
                if y == 7:
                    if x == 0 or x == 7:
                        self.white_pieces.add(Rook(scaled_x,scaled_y, "rook", "w")) 
                    if x == 1 or x == 6:
                        self.white_pieces.add(Knight(scaled_x,scaled_y, "knight", "w")) 
                    if x == 2 or x == 5:
                        self.white_pieces.add(Bishop(scaled_x,scaled_y, "bishop", "w"))
                    if x == 3:
                        self.white_pieces.add(Queen(scaled_x,scaled_y, "queen", "w"))
                    if x == 4:
                        self.white_pieces.add(King(scaled_x,scaled_y, "king", "w"))
                if y==1:
                    self.black_pieces.add(Pawn(scaled_x,scaled_y, "pawn", "b"))
                if y == 6:
                    self.white_pieces.add(Pawn(scaled_x,scaled_y, "pawn", "w"))
        self.all_sprites.add(self.white_pieces,self.black_pieces)

    def draw_board(self):
        self.screen.fill((0,0,0))        
        for x in range(len(self.lauta)):
            for y in range(len(self.lauta)):
                square = self.lauta[x][y]
                self.screen.blit(self.tiles[square],(x*self.scale, y*self.scale))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()       
    
    def downscale(self, position):
        return position//self.scale

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    starting_pos = pygame.mouse.get_pos()
                    self.chosen_piece = self.all_sprites.get_sprites_at(starting_pos)
                    if self.chosen_piece == []:
                        continue
                    if self.chosen_piece[0].color == "w" and self.white_to_move:
                        self.chosen_piece_original_position = starting_pos
                    if self.chosen_piece[0].color == "b" and not self.white_to_move:
                        self.chosen_piece_original_position = starting_pos
            #if event.type == pygame.MOUSEMOTION:
                #if self.chosen_piece != []:
                    #coord = event.rel
                    #self.chosen_piece[0].move_ip(coord[0],coord[1])
            if event.type == pygame.MOUSEBUTTONUP:
                coord_on_mbup = event.pos
                if event.button == 1:
                    if self.chosen_piece != []:
                        if self.chosen_piece_original_position != None:
                            dx_np = self.downscale(coord_on_mbup[0])
                            dy_np = self.downscale(coord_on_mbup[1])
                            dx_op = (self.downscale(self.chosen_piece_original_position[0]))
                            dy_op = (self.downscale(self.chosen_piece_original_position[1]))
                            dx = dx_np-dx_op
                            dy = dy_np-dy_op
                            if self.can_move(dx,dy):
                                self.chosen_piece[0].move_ip(dx,dy, self.scale)
                                if self.white_to_move:
                                    pygame.sprite.groupcollide(self.white_pieces,self.black_pieces,False,True)
                                else:
                                    pygame.sprite.groupcollide(self.white_pieces,self.black_pieces,True,False)
                                self.trigger_turn()
                    self.chosen_piece_original_position = None
                    self.chosen_piece = []
    
    def trigger_turn(self):
        if self.white_to_move:
            self.white_to_move = False
        else:
            self.white_to_move=True

    def can_move(self,dx=0,dy=0):
        move_is_legal = False
        taking = False
        if isinstance(self.chosen_piece[0], Pawn):
            if self.chosen_piece[0].color == "w":
                if dy == -1:
                    if dx == 1 or dx == -1:
                        taking = True
                        move_is_legal = True
                    if dx == 0:
                        move_is_legal = True
                if dy == -2 and dx == 0:
                    #check for moved todo
                    move_is_legal = True
            if self.chosen_piece[0].color == "b":
                if dy == 1:
                    if dx == 1 or dx ==-1:
                        taking =True
                        move_is_legal = True
                    if dx == 0:
                        move_is_legal = True
                if dy == 2 and dx == 0:
                    #check for moved todo
                    move_is_legal = True
        if not move_is_legal:
            return False
        

        self.chosen_piece[0].rect.move_ip(dx*self.scale,dy*self.scale)

        if self.chosen_piece[0].color == "w":
            self.white_pieces.remove(self.chosen_piece[0])
            collide_same_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.white_pieces,False)
            collide_diff_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.black_pieces,False)
            self.white_pieces.add(self.chosen_piece[0])
        if self.chosen_piece[0].color == "b":
            self.black_pieces.remove(self.chosen_piece[0])
            collide_same_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.black_pieces,False)
            collide_diff_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.white_pieces,False)
            self.black_pieces.add(self.chosen_piece[0])
        
        self.chosen_piece[0].rect.move_ip(-dx*self.scale,-dy*self.scale)

        if taking and not collide_diff_color:
            return False
        if not taking and collide_diff_color:
            return False
        
        return not collide_same_color        

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_board()