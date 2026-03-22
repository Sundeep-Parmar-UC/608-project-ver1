# receive UserMove
# receive BotMove
# receive complete Board layout

#use magic (or source/destination pairs from user and bot))
#check for castle situation
#check for en passant situation


#return new Board layout with updated moves

def board(UserMove, BotMove, BoardLayout):
    # figure out turn
    if not UserMove:
        move = BotMove
        turn = "Black"
    else:
        move = UserMove
        turn = "White"
    
    # check for castling
    if move == "O-O":  # kingside
        if turn == "White":
            BoardLayout[0][4] = "0"
            BoardLayout[0][7] = "0"
            BoardLayout[0][6] = "k"
            BoardLayout[0][5] = "r"
    
        elif turn == "Black":
            BoardLayout[7][4] = "0"
            BoardLayout[7][7] = "0"
            BoardLayout[7][6] = "K"
            BoardLayout[7][5] = "R"
    
    elif move == "O-O-O":  # queenside
        if turn == "White":
            BoardLayout[0][4] = "0"
            BoardLayout[0][0] = "0"
            BoardLayout[0][2] = "k"
            BoardLayout[0][3] = "r"
    
        elif turn == "Black":
            BoardLayout[7][4] = "0"
            BoardLayout[7][0] = "0"
            BoardLayout[7][2] = "K"
            BoardLayout[7][3] = "R"
    
    else:
        # remove piece letter if present, like N in Ng8-f6
        if move[0].upper() in ["N", "B", "R", "Q", "K"]:
            move = move[1:]
    
        # remove hyphen, like c2-c4 -> c2c4
        move = move.replace("-", "")
    
        if len(move) == 4 or len(move) == 5:
            start_col = ord(move[0]) - ord('a')
            start_row = int(move[1]) - 1
    
            end_col = ord(move[2]) - ord('a')
            end_row = int(move[3]) - 1
    
            piece = BoardLayout[start_row][start_col]
    
            # check for en passant
    
            # white pawn (lowercase)
            if piece == "p" and end_row == start_row + 1 and abs(end_col - start_col) == 1 and BoardLayout[end_row][end_col] == "0" and BoardLayout[start_row][end_col] == "P":
                BoardLayout[end_row][end_col] = "p"
                BoardLayout[start_row][start_col] = "0"
                BoardLayout[start_row][end_col] = "0"
    
            # black pawn (uppercase)
            elif piece == "P" and end_row == start_row - 1 and abs(end_col - start_col) == 1 and BoardLayout[end_row][end_col] == "0" and BoardLayout[start_row][end_col] == "p":
                BoardLayout[end_row][end_col] = "P"
                BoardLayout[start_row][start_col] = "0"
                BoardLayout[start_row][end_col] = "0"
    
            else:
                # normal move
                BoardLayout[end_row][end_col] = piece
                BoardLayout[start_row][start_col] = "0"
    
                # check for pawn promotion
    
                # white promotion
                if piece == "p" and end_row == 7:
                    if len(move) == 5:
                        BoardLayout[end_row][end_col] = move[4].lower()
                    else:
                        BoardLayout[end_row][end_col] = "q"
    
                # black promotion
                elif piece == "P" and end_row == 0:
                    if len(move) == 5:
                        BoardLayout[end_row][end_col] = move[4].upper()
                    else:
                        BoardLayout[end_row][end_col] = "Q"
    return BoardLayout