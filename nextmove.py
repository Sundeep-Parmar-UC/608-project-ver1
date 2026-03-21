# receive board layout
# receive Moves String
# receive user move
# receive SQL connector

# construction user move with Moves string
# prepare SQL statement
# obtain list of all next moves
#build metric
#decide next move
#call baord update function

#return next botmove, metricarray, board layout
import board as bd

def nextmove(BoardLayout,MovesArray,UserMove,SQLconnect):
    Metrics = ["# of Games to consider","# of Unique Moves to Consider"]
    BotMove = ""

    
    bd.board(UserMove, BotMove, BoardLayout)

    return BotMove,Metrics,BoardLayout