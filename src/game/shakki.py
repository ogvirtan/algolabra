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
                        self.black_pieces.add(Rook(scaled_x,scaled_y, "rook", "b", self.scale)) 
                    if x == 1 or x == 6:
                        self.black_pieces.add(Knight(scaled_x,scaled_y, "knight", "b", self.scale)) 
                    if x == 2 or x == 5:
                        self.black_pieces.add(Bishop(scaled_x,scaled_y, "bishop", "b", self.scale))
                    if x == 3:
                        self.black_pieces.add(Queen(scaled_x,scaled_y, "queen", "b", self.scale))
                    if x == 4:
                        self.black_pieces.add(King(scaled_x,scaled_y, "king", "b", self.scale))
                if y == 7:
                    if x == 0 or x == 7:
                        self.white_pieces.add(Rook(scaled_x,scaled_y, "rook", "w", self.scale)) 
                    if x == 1 or x == 6:
                        self.white_pieces.add(Knight(scaled_x,scaled_y, "knight", "w", self.scale)) 
                    if x == 2 or x == 5:
                        self.white_pieces.add(Bishop(scaled_x,scaled_y, "bishop", "w", self.scale))
                    if x == 3:
                        self.white_pieces.add(Queen(scaled_x,scaled_y, "queen", "w", self.scale))
                    if x == 4:
                        self.white_pieces.add(King(scaled_x,scaled_y, "king", "w", self.scale))
                if y==1:
                    self.black_pieces.add(Pawn(scaled_x,scaled_y, "pawn", "b", self.scale))
                if y == 6:
                    self.white_pieces.add(Pawn(scaled_x,scaled_y, "pawn", "w", self.scale))
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
                            if dx == dy == 0:
                                continue
                            if self.can_move(dx,dy):
                                self.chosen_piece[0].move_ip(dx,dy, self.scale)
                                self.chosen_piece[0].update_position(dx,dy)
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
        bools = self.move_is_legal(dx,dy)
        legal_move =  bools[0]
        taking = bools[1]

        if not legal_move:
            return False        

        collide_or_not = self.check_collision_destination(dx,dy)#False means collision

        if isinstance(self.chosen_piece[0], Pawn):
            if taking and not self.check_collision_diff_color(dx,dy):
                return True
        
        if isinstance(self.chosen_piece[0], Rook):
            if not self.occupied_squares_inbetween_line(dx,dy):
                return False
            if not self.check_collision_diff_color(dx,dy):
                return True
        
        if isinstance(self.chosen_piece[0], Bishop):
            if not self.occupied_squares_in_diagonal(dx,dy):
                return False
            if not self.check_collision_diff_color(dx,dy):
                return True
        
        if isinstance(self.chosen_piece[0], Queen):
            print(dx,dy," queen dx and dy")
            if abs(dx) == abs(dy):
                if not self.occupied_squares_in_diagonal(dx,dy):
                    return False
                if not self.check_collision_diff_color(dx,dy):
                    return True
            if dy == 0 or dx == 0:
                if not self.occupied_squares_inbetween_line(dx,dy):
                    return False
                if not self.check_collision_diff_color(dx,dy):
                    return True
        
        print(self.chosen_piece[0].position, collide_or_not)

        return collide_or_not      
    
    def check_collision_destination(self, dx, dy):
        coll_diff = self.check_collision_diff_color(dx,dy)
        coll_same = self.check_collision_same_color(dx,dy)

        if not coll_diff or not coll_same:
            return False
        return True
    
    def check_collision_diff_color(self, dx, dy):
        self.chosen_piece[0].rect.move_ip(dx*self.scale,dy*self.scale)

        if self.chosen_piece[0].color == "w":
            self.white_pieces.remove(self.chosen_piece[0])
            collide_diff_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.black_pieces,False)
            self.white_pieces.add(self.chosen_piece[0])
        elif self.chosen_piece[0].color == "b":
            self.black_pieces.remove(self.chosen_piece[0])
            collide_diff_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.white_pieces,False)
            self.black_pieces.add(self.chosen_piece[0])
        
        self.chosen_piece[0].rect.move_ip(-dx*self.scale,-dy*self.scale)

        return not collide_diff_color
    
    def check_collision_same_color(self, dx, dy):
        self.chosen_piece[0].rect.move_ip(dx*self.scale,dy*self.scale)

        if self.chosen_piece[0].color == "w":
            self.white_pieces.remove(self.chosen_piece[0])
            collide_same_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.white_pieces,False)
            self.white_pieces.add(self.chosen_piece[0])
        elif self.chosen_piece[0].color == "b":
            self.black_pieces.remove(self.chosen_piece[0])
            collide_same_color = pygame.sprite.spritecollide(self.chosen_piece[0],self.black_pieces,False)
            self.black_pieces.add(self.chosen_piece[0])
        
        self.chosen_piece[0].rect.move_ip(-dx*self.scale,-dy*self.scale)

        return not collide_same_color
    
    def occupied_squares_inbetween_line(self, dx, dy):
        rval = True
        if dy == 0:
            dxnegativecorrector = 1
            if dx < 0:
                dxnegativecorrector = -1
            for location in range(1,abs(dx)):
                if self.check_collision_destination(dxnegativecorrector*location, dy):
                    continue
                else:
                    rval = False
        else:
            dynegativecorrector = 1
            if dy <0:
                dynegativecorrector = -1
            for location in range(1,abs(dy)):
                if self.check_collision_destination(dx, dynegativecorrector*location):
                    continue
                else:
                    rval = False
        return rval
            

    def occupied_squares_in_diagonal(self,dx,dy):
        rval = True
        dxnegativecorrector = 1
        dynegativecorrector = 1
        if dx < 0:
            dxnegativecorrector = -1
        if dy < 0:
            dynegativecorrector = -1
        for location in range(1,abs(dx)):
            if self.check_collision_destination(dxnegativecorrector*location, dynegativecorrector*location):
                continue
            else:
                rval = False
        return rval
    
    def move_is_legal(self, dx, dy):
        pawn_taking = True
        legality = False
        if isinstance(self.chosen_piece[0], Pawn):
            pawn_taking = False
            if self.chosen_piece[0].color == "w":
                if dy == -1:
                    if dx == 1 or dx == -1:
                        pawn_taking = True
                        legality = True
                    if dx == 0:
                        legality = True
                if dy == -2 and dx == 0:
                    if self.chosen_piece[0].position[1] == 6:
                        legality = True
            if self.chosen_piece[0].color == "b":
                if dy == 1:
                    if dx == 1 or dx ==-1:
                        pawn_taking =True
                        legality = True
                    if dx == 0:
                        legality = True
                if dy == 2 and dx == 0:
                    if self.chosen_piece[0].position[1] == 1:
                        legality = True
        if isinstance(self.chosen_piece[0], Bishop):
            if abs(dy) == abs(dx):
                legality = True
        if isinstance(self.chosen_piece[0], King):
            if abs(dy)<= 1 and abs(dx)<= 1:
                legality =True
        if isinstance(self.chosen_piece[0], Knight):
            if abs(dy) == 2 and abs(dx) == 1:
                legality = True
            elif abs(dy) == 1 and abs(dx) == 2:
                legality = True
        if isinstance(self.chosen_piece[0], Rook):
            if abs(dx) >0 and dy == 0:
                legality = True
            elif abs(dy) > 0 and dx == 0:
                legality = True
        if isinstance(self.chosen_piece[0], Queen):
            if abs(dx) > 0 and dy == 0:
                legality = True
            elif abs(dy) > 0 and dx == 0:
                legality = True
            elif abs(dy) == abs(dx):
                legality = True

        return (legality, pawn_taking)

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_board()