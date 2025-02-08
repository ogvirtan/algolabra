from entities.piece import Piece

class Pawn(Piece):

    def init(self):
        super().__init__()
        
    
    def move_ip(self, dx = 0, dy=0, scale=128):
        #if dx == 1 or -1:
            #self.take(dx,dy,scale)
        if self.color == "w":
            self.rect.move_ip(dx*scale,dy*scale)
        else:
            self.rect.move_ip(dx*scale,dy*scale)