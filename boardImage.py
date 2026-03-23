# receive complete Board layout
# receive boardspace location as int,int

# deteremine status of piece and board colour on board space location
# construction ImageName of space based of naming convention

# return ImageName to display

def boardImage(BoardLayout, BoardSpace):

    col = ord(BoardSpace[0]) - ord('a')
    row = int(BoardSpace[1]) - 1

    piece = BoardLayout[row][col]

    # determine square color
    if (row + col) % 2 == 0:
        square_color = "White"
    else:
        square_color = "Black"

    # empty square
    if piece == "0":
        ImageName = f"ChessBoard/{square_color}.jpg"

    else:
        # determine piece color
        if piece.islower():
            piece_color = "White"
        else:
            piece_color = "Black"

        # determine piece type
        piece_type_map = {
            "p": "Pawn",
            "r": "Rook",
            "n": "Knight",
            "b": "Bishop",
            "q": "Queen",
            "k": "King"
        }

        piece_type = piece_type_map[piece.lower()]

        ImageName = f"ChessBoard/{piece_color}_{piece_type}_{square_color}.jpg"

    return ImageName