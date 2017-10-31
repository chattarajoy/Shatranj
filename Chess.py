# coding=utf-8
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYUP, K_ESCAPE
from sys import exit

from ChessPieces import *


# noinspection PyUnusedLocal
def game():
    # The Game loop
    Mousedown2 = False
    Mousedown = False
    Mousereleased = False
    TargetPiece = None
    checkmate = False
    check = False
    teams = ['white', 'black']

    while True:
        turn = teams[0]
        checkquitgame()
        pieceholder = None
        if checkmate:
            # game over
            drawboard([gray, violet])
        else:
            drawboard(colors)

        # get cursor
        Cursor = pygame.mouse.get_pos()
        # check for any events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                Mousedown = True
                Mousedown2 = True
            if event.type == MOUSEBUTTONUP:
                Mousedown = False
                Mousereleased = True

        # pickup the nearest piece if a piece is not selected
        if Mousedown and not TargetPiece:
            TargetPiece = nearest_piece(Cursor, Pieces)
            if TargetPiece:
                OriginalPlace = TargetPiece.square

        if Mousedown2 and TargetPiece:
            TargetPiece.drag(Cursor)

        if Mousereleased:
            Mousereleased = False
            Mousedown2 = False
            if TargetPiece and TargetPiece.team != turn:  # check your turn
                TargetPiece.update(OriginalPlace)
                TargetPiece = None
            elif TargetPiece:
                pos1 = TargetPiece.rect.center
                for Square in squareCenters:
                    if distance_formula(pos1, Square.center) < BoardWidth / 16:  # half width of square
                        newspot = Square
                        otherpiece = nearest_piece(Square.center, Pieces)

                for piece in Pieces:
                    if type(piece) == King and piece.team == turn:
                        check = piece.undercheck()
                        checkmate = piece.checkforcheckmate()
                        if checkmate:
                            continue

                if otherpiece and otherpiece != TargetPiece \
                        and otherpiece.team == TargetPiece.team:

                    # check if space is occupied by team
                    TargetPiece.update(OriginalPlace)
                    if check:
                        teams = teams[::-1]  # tempfix
                elif newspot not in TargetPiece.movelist():

                    # check if you can move there
                    TargetPiece.update(OriginalPlace)
                    if check:
                        teams = teams[::-1]  # tempfix
                elif otherpiece and otherpiece != TargetPiece \
                        and type(otherpiece) != King:

                    # take enemy piece
                    for piece in Pieces:
                        if piece == otherpiece:
                            pieceholder = piece  # temp
                            Pieces.remove(piece)
                            TargetPiece.update(newspot)
                    teams = teams[::-1]  # switch teams
                else:
                    # move
                    TargetPiece.update(newspot)
                    if type(TargetPiece) == Pawn or type(TargetPiece) \
                            == BlackPawn or type(TargetPiece) == King:
                        TargetPiece.bool += 1
                    teams = teams[::-1]  # switch teams

                if True:  # always check every turn at end
                    for piece in Pieces:
                        if type(piece) == King and piece.team == turn:
                            check = piece.undercheck()
                if check:
                    # if still under check revert back
                    TargetPiece.update(OriginalPlace)
                    if pieceholder and pieceholder.team != TargetPiece.team:
                        Pieces.append(pieceholder)
                        # noinspection PyUnusedLocal
                        pieceholder = None
                    if type(TargetPiece) == Pawn or type(TargetPiece) == BlackPawn or type(TargetPiece) == King:
                        TargetPiece.bool -= 1
                    teams = teams[::-1]  # switch back
            TargetPiece = None
        for piece in Pieces:
            piece.draw(screen)
        pygame.display.flip()


def checkquitgame():
    for _ in pygame.event.get(QUIT):
        print len(squareCenters)
        pygame.quit()
        exit()

    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            exit()
        pygame.event.post(event)


pygame.display.set_caption('Shatranj')
FPS = pygame.time.Clock()
FPS.tick(120)

if __name__ == '__main__':
    game()
