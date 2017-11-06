# coding=utf-8
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from ChessPieces import *


# noinspection PyUnusedLocal
def game():
    # The Game loop
    SHOW_END_GAME = 1
    Mousedown2 = False
    Mousedown = False
    Mousereleased = False
    TargetPiece = None
    checkmate = False
    check_message = False
    check = False
    teams = ['white', 'black']
    colors = [dark_brown, light_brown]
    drawboard(colors)

    while True:
        turn = teams[0]
        checkquitgame()
        pieceholder = None

        for piece in Pieces:
            if type(piece) == King and piece.team == turn:
                check = piece.undercheck()
                if not check:
                    check_message = False
                if piece.checkforcheckmate():
                    checkmate = True

        if checkmate:
            # game over
            colors = [gray, violet]
            drawboard(colors)
            if SHOW_END_GAME:
                show_checkmate(teams)
                SHOW_END_GAME = 0
        elif check and not check_message:
            show_check(teams)
            check_message = True
            continue

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


pygame.display.set_caption('Shatranj')
FPS = pygame.time.Clock()
FPS.tick(30)

if __name__ == '__main__':
    game()
