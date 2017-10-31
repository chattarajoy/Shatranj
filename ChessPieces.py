import pygame

from helperfunctions import *


class ChessPiece(pygame.sprite.Sprite):
    # class for pieces

    def __init__(self, image, position, team):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (BoardWidth / 8 - BoardWidth / 21, BoardWidth / 8 - BoardWidth / 21))
        self.square = position
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.topleft = position.topleft
        self.rect.center = position.center

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def drag(self, cursor):
        self.rect.center = cursor

    def update(self, position):
        self.square = position
        self.rect.center = position.center

    def movelist(self):
        return squareCenters


class Pawn(ChessPiece):
    def __init__(self, image, position, team):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0

    def movelist(self):
        move_list = []
        removeupto = []
        noblocks = make_lines(self.square, squareCenters, [math.pi / 2])
        takeblocks = make_lines(self.square, squareCenters, [math.pi
                                                             / 4, 3 * math.pi / 4])
        if self.bool <= 0:
            for (x, y) in noblocks:
                move_list.append(x)
                move_list = move_list[len(move_list) - 2:len(move_list)]
        else:
            for (x, y) in make_lines(self.square, squareCenters,
                                     [math.pi / 2]):
                move_list.append(x)
            move_list = move_list[len(move_list) - 1:len(move_list)]
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
                    if item[0] in move_list:
                        move_list.remove(item[0])
        for x in move_list:
            for (a, b) in removeupto:
                if isfarther(self.square, a, x):
                    move_list.remove(x)
        for (block, angle) in takeblocks:
            if block.colliderect(self.square):
                for piece in Pieces:
                    if piece.square == block:
                        move_list.append(block)
        return move_list


class BlackPawn(Pawn):
    def movelist(self):
        move_list = []
        removeupto = []
        noblocks = make_lines(self.square, squareCenters, [-math.pi
                                                           / 2])
        takeblocks = make_lines(self.square, squareCenters, [-math.pi
                                                             / 4, -3 * math.pi / 4])
        if self.bool <= 0:
            for (x, y) in noblocks:
                move_list.append(x)
            move_list = move_list[0:2]
        else:
            for (x, y) in make_lines(self.square, squareCenters,
                                     [-math.pi / 2]):
                move_list.append(x)
            move_list = move_list[0:1]
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
                    if item[0] in move_list:
                        move_list.remove(item[0])
        for x in move_list:
            for (a, b) in removeupto:
                if isfarther(self.square, a, x):
                    move_list.remove(x)
        for (block, angle) in takeblocks:
            if block.colliderect(self.square):
                for piece in Pieces:
                    if piece.square == block:
                        move_list.append(block)
        return move_list


class Bishop(ChessPiece):
    def movelist(self):
        removeupto = []
        noblocks = make_lines(self.square, squareCenters, [math.pi / 4,
                                                           3 * math.pi / 4, -math.pi / 4, -3
                                                           * math.pi / 4])
        move_list = []
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
        for item in noblocks:
            move_list.append(item[0])
        for (x, y) in noblocks:
            for (a, b) in removeupto:
                if isfarther(self.square, a, x) and y == b and x \
                        in move_list:
                    move_list.remove(x)
        return move_list


class Knight(ChessPiece):
    def movelist(self):
        move_list = []
        noblocks = make_lines(self.square, squareCenters, [
            math.atan2(1, 2),
            math.atan2(2, 1),
            math.atan2(1, -2),
            math.atan2(-2, 1),
            math.atan2(-1, -2),
            math.atan2(-2, -1),
            math.atan2(-1, 2),
            math.atan2(2, -1),
        ])
        adjacent = []
        for Square in squareCenters:
            if Square.colliderect(self.square):
                adjacent.append(Square)
        for Square in adjacent:
            for item in noblocks:
                if Square.colliderect(item[0]):
                    move_list.append(item[0])
        return move_list


class Rook(ChessPiece):
    def movelist(self):
        removeupto = []
        noblocks = make_lines(self.square, squareCenters, [math.pi,
                                                           math.pi / 2, 0, -math.pi / 2])
        move_list = []
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
        for item in noblocks:
            move_list.append(item[0])
        for (x, y) in noblocks:
            for (a, b) in removeupto:
                if isfarther(self.square, a, x) and y == b and x \
                        in move_list:
                    move_list.remove(x)
        return move_list


class Queen(ChessPiece):
    def movelist(self):
        removeupto = []
        noblocks = make_lines(self.square, squareCenters, [
            math.pi,
            math.pi / 2,
            0,
            -math.pi / 2,
            math.pi / 4,
            3 * math.pi / 4,
            -math.pi / 4,
            -3 * math.pi / 4,
        ])
        move_list = []
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
        for item in noblocks:
            move_list.append(item[0])
        for (x, y) in noblocks:
            for (a, b) in removeupto:
                if isfarther(self.square, a, x) and y == b and x \
                        in move_list:
                    move_list.remove(x)
        return move_list


class King(ChessPiece):
    def __init__(
            self,
            image,
            position,
            team,
    ):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0  # can castle?

    def movelist(self):
        make_lines(self.square, squareCenters, [
            math.pi,
            math.pi / 2,
            0,
            -math.pi / 2,
            math.pi / 4,
            3 * math.pi / 4,
            -math.pi / 4,
            -3 * math.pi / 4,
        ])
        move_list = []
        for Square in squareCenters:
            for piece in Pieces:
                if Square.colliderect(self.square):
                    move_list.append(Square)
                elif Square in move_list and piece.team != self.team \
                        and Square in piece.movelist():
                    move_list.remove(Square)

        for piece in Pieces:
            if piece.square in move_list and piece.team == self.team:
                move_list.remove(piece.square)
        return move_list

    def undercheck(self):
        for piece in Pieces:
            if self.square in piece.movelist() and piece.team \
                    != self.team:
                return True
        return False

    def checkforcheckmate(self):
        if self.undercheck() and self.movelist() == []:
            return True
        else:
            return False

# draw board so that pieces can be initialized
drawboard(colors)

# initialize pieces
Pieces = [
    Pawn('MEDIA\WhitePawn.png', squareCenters[48], 'white'),
    Pawn('MEDIA\WhitePawn.png', squareCenters[49], 'white'),
    Pawn('MEDIA\WhitePawn.png', squareCenters[50], 'white'),
    Pawn('MEDIA\WhitePawn.png', squareCenters[51], 'white'),
    Pawn('MEDIA\WhitePawn.png', squareCenters[52], 'white'),
    Pawn('MEDIA\WhitePawn.png', squareCenters[53], 'white'),
    Pawn('MEDIA\WhitePawn.png', squareCenters[54], 'white'),
    Pawn('MEDIA\WhitePawn.png', squareCenters[55], 'white'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[8], 'black'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[9], 'black'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[10], 'black'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[11], 'black'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[12], 'black'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[13], 'black'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[14], 'black'),
    BlackPawn('MEDIA\BlackPawn.png', squareCenters[15], 'black'),
    Bishop('MEDIA\WhiteBishop.png', squareCenters[58], 'white'),
    Bishop('MEDIA\WhiteBishop.png', squareCenters[61], 'white'),
    Bishop('MEDIA\BlackBishop.png', squareCenters[2], 'black'),
    Bishop('MEDIA\BlackBishop.png', squareCenters[5], 'black'),
    Knight('MEDIA\WhiteKnight.png', squareCenters[57], 'white'),
    Knight('MEDIA\WhiteKnight.png', squareCenters[62], 'white'),
    Knight('MEDIA\BlackKnight.png', squareCenters[1], 'black'),
    Knight('MEDIA\BlackKnight.png', squareCenters[6], 'black'),
    Rook('MEDIA\WhiteRook.png', squareCenters[56], 'white'),
    Rook('MEDIA\WhiteRook.png', squareCenters[63], 'white'),
    Rook('MEDIA\BlackRook.png', squareCenters[0], 'black'),
    Rook('MEDIA\BlackRook.png', squareCenters[7], 'black'),
    King('MEDIA\BlackKing.png', squareCenters[4], 'black'),
    King('MEDIA\WhiteKing.png', squareCenters[60], 'white'),
    Queen('MEDIA\BlackQueen.png', squareCenters[3], 'black'),
    Queen('MEDIA\WhiteQueen.png', squareCenters[59], 'white'),
]
