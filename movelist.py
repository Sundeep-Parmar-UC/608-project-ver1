# receive UserMove
def receive_UserMove(UserMove: str, MoveTable: list): 
    MoveTable = movelist(UserMove, None, MoveTable)
    return MoveTable   #return the updated MoveTable after processing user's move

# receive BotMove
def receive_BotMove(BotMove: str, MoveTable: list):
    MoveTable = movelist(None, BotMove, MoveTable)
    return MoveTable

# receive complete Move Table
def receive_complete_MoveTable(MoveTable: list):
    MoveTable = movelist(None, None, MoveTable)
    return MoveTable

#use magic (or source/destination pairs from user and bot))


#check for castle situation 
def get_move(move: str):
    source = move[:2]   #first 2 char
    dest = move[2:]     #last 3 char
    return source, dest

#check if castling
def is_castling(source, dest):
    return (source == "e1" and dest in ("g1", "c1")) or \
           (source == "e8" and dest in ("g8", "c8"))

    if is_castling(source, dest):
        MoveTable.append({"type": "castling", "move": move})
        return MoveTable


#check for en passant situation 

#return new MoveTable with updated moves

def movelist(UserMove, BotMove, MoveTable):

    
    return MoveTable
