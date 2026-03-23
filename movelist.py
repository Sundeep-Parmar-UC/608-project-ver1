def movelist(AllMovesString):
    #1. split input  PGN-style MovesString into tokens
    tokens = AllMovesString.split()
    
    #2. Skip move numbers "1.", "2." etc.
    moves = [t for t in tokens if not t.endswith(".")]

    #3. Build movelist html-ready MoveTable
    MoveTable = []
    for idx, move in enumerate(moves):
        if idx % 2 == 0:  # even index=UserMove
            MoveNumber = len(MoveTable)+1
            row = [str(MoveNumber),move, '']
            MoveTable.append(row)
        
        else:  # odd index=BotMove
            MoveTable[-1][2] = move
    
    return MoveTable


