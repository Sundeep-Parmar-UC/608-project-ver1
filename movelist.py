# func to receive UserMove
def receive_UserMove(UserMove: str, MoveTable: list): 
    return movelist(UserMove, None, MoveTable)  

# func to receive BotMove
def receive_BotMove(BotMove: str, MoveTable: list):
    return movelist(None, BotMove, MoveTable)

# func to receive complete MoveTable
def receive_complete_MoveTable(MoveTable: list):
    return movelist(None, None, MoveTable)
    
# func to get source/destination square for user/bot
def get_move(move: str):
    source = move[:2]   #first 2 char
    dest = move[2:]     #last 2 char
    return source, dest

# func to check for castling situation (in UCI notation)
def is_castling(source, dest):
    return (source == "e1" and dest in ("g1", "c1")) or (source == "e8" and dest in ("g8", "c8"))

# func to check for en passant situation (4 criterias to check)
def is_en_passant(source, dest, MoveTable):
    # 1: pawn moves diagonally = col and row changes by 1
    col_change = abs(ord(source[0]) - ord(dest[0])) == 1
    row_change = abs(int(source[1]) - int(dest[1])) == 1

    if not (col_change and row_change):
        return False

    # 2: if no previous move, cannot be en passant (ie. dest square is empty)
    if not MoveTable:
        return False

    last_move = MoveTable[-1]["move"]
    last_src, last_dst = get_move(last_move)

    # 3: last move must be a 2‑square pawn advance
    if abs(int(last_src[1]) - int(last_dst[1])) != 2:
        return False

    # 4: destination col must match the pawn that jumped
    return dest[0] == last_dst[0]

#------------------------------------------------------------------------------#
# parse MovesString
def parse_MoveString(AllMovesString):
    tokens = AllMovesString.split()
    moves = []

    for token in tokens:
        # Skip move numbers "1.", "2." etc.
        if token.endswith("."):
            continue
        moves.append(token)

    return moves
#------------------------------------------------------------------------------#
# process MovesString input
def process_MovesString(MovesString):
    MoveTable = []
    for idx, move in enumerate(MovesString):
        if idx % 2 == 0:
            # even index=UserMove
            MoveTable = receive_UserMove(move, MoveTable)
        else:
            # odd index=BotMove
            MoveTable = receive_BotMove(move, MoveTable)
    return MoveTable
#------------------------------------------------------------------------------#
# return new MoveTable with updated moves
def movelist(UserMove, BotMove, MoveTable):
    # move = [
    #     '<td style="padding: 6px; border: 2px solid #ddd; font-weight: bold;">','1',
    #     '</td><td style="padding: 6px; border: 2px solid #ddd;">', UserMove,
    #     '</td><td style="padding: 6px; border: 2px solid #ddd;">', BotMove, 
    #     '</td>'
    # ]
    
    # Case 1: UserMove arrives, start a new row
    if UserMove:
        MoveNumber = len(MoveTable) + 1
        MoveTable.append({
            "MoveNumber": str(MoveNumber),
            "UserMove": UserMove,
            "BotMove": ""
        })
        return MoveTable

    # Case 2: BotMove arrives, fill the last row
    if BotMove:
        if not MoveTable:
            # Safety: BotMove cannot appear first
            MoveTable.append({
                "MoveNumber": "1",
                "UserMove": "",
                "BotMove": BotMove
            })
        else:
            MoveTable[-1]["BotMove"] = BotMove

    return MoveTable