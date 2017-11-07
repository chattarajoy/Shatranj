# coding=utf-8
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from ChessPieces import *


# noinspection PyUnusedLocal
def game():
    # The Game loop
    SHOW_END_GAME = 1
    Mousedown = False
    Mousereleased = False
    TargetPiece = None
    checkmate = False
    check_message = False
    check = False
    teams = ['White', 'Black']
    colors = [dark_brown, light_brown]
    drawboard(colors)

    while True:
        turn = teams[0]
        checkquitgame()
        pieceholder = None

        # --------      CHECK FOR CHECKMATE AND CHECK CONDITIONS --------
        for piece in Pieces:
            if type(piece) == King and piece.team == turn:
                check = piece.undercheck()
                if not check:
                    check_message = False
                checkmate = piece.checkforcheckmate()

        if checkmate:
            colors = [gray, violet]
            drawboard(colors)
            if SHOW_END_GAME:
                show_checkmate(teams)
                SHOW_END_GAME = 0

        elif check and not check_message:
            show_check(teams)
            check_message = True
            continue

        # ----- END CHECKING ----

        drawboard(colors)

        # get cursor
        Cursor = pygame.mouse.get_pos()

        # ---- BLOCKING CALL ----
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                Mousedown = True
            if event.type == MOUSEBUTTONUP:
                Mousedown = False
                Mousereleased = True

        # ---- Events on MouseDown -----
        # pickup the nearest piece if a piece is not selected
        if Mousedown and not TargetPiece:
            TargetPiece = nearest_piece(Cursor, Pieces)
            if TargetPiece:
                OriginalPlace = TargetPiece.square

        if Mousedown and TargetPiece:
            TargetPiece.drag(Cursor)

        # ---- MouseReleased Events -----
        if Mousereleased:
            Mousereleased = False

            # ----- validate turn -----
            if TargetPiece and TargetPiece.team != turn:  # check your turn
                TargetPiece.update(OriginalPlace)
                TargetPiece = None

            # ---- set closest piece that taken be taken ----
            elif TargetPiece:
                pos1 = TargetPiece.rect.center
                for Square in squareCenters:
                    if distance_formula(pos1, Square.center) < BoardWidth / 16:  # half width of square
                        newspot = Square
                        otherpiece = nearest_piece(Square.center, Pieces)
                        break

                if otherpiece and otherpiece != TargetPiece and otherpiece.team == TargetPiece.team:

                    # check if space is occupied by team
                    TargetPiece.update(OriginalPlace)

                elif newspot not in TargetPiece.movelist():

                    # check if you can move there
                    TargetPiece.update(OriginalPlace)

                elif otherpiece and otherpiece != TargetPiece and type(otherpiece) != King:
                    # take enemy piece
                    for piece in Pieces:
                        if piece == otherpiece:
                            pieceholder = piece
                            Pieces.remove(piece)
                            TargetPiece.update(newspot)
                    teams = teams[::-1]  # switch teams
                else:
                    # move
                    TargetPiece.update(newspot)
                    if type(TargetPiece) == Pawn or type(TargetPiece) == BlackPawn or type(TargetPiece) == King:
                        TargetPiece.bool += 1
                    teams = teams[::-1]  # switch teams

                if True:  # always check every turn at end
                    check = False
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
                    teams = teams[::-1]  # switch back
            TargetPiece = None

        for piece in Pieces:
            piece.draw(screen)
        pygame.display.flip()


pygame.display.set_caption('Shatranj')
FPS = pygame.time.Clock()
FPS.tick(10)

if __name__ == '__main__':
    game()
