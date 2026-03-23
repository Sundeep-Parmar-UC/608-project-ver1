#	Breakdown moves string
#	Construct move_array
#		Set5, Set10, Set15,Set20,Set30,Set40,Set70,Set_Remain
#	Return [move_array] 

import re
import chess.pgn
import io

def ParserMove(movesPGN):

    movesPGN = re.sub(r"\{ \[%eval \d\.\d\d\] \}", "", movesPGN)
    movesPGN = re.sub(r"\{ \[%clk \d\.\d\d\] \}", "", movesPGN)
    movesPGN = movesPGN.replace("...", ".")
    
    # Use regex to extract moves and move counts
    #moves_Piece_array = re.findall(r'\d+\.\s+([^\s]+)\s+([^\s]+)', moves)

    #at this point chess moves are in PGN notation,  convert to LAN (long algebraic)
    movesArray = pgn_to_coordinates(movesPGN)

    NumberOfMoves = len(movesArray)
    MoveNumber = 1 
    WhiteMove = True
    moves = ""
    for row in movesArray:
        if WhiteMove:
            WhiteMove = False
            moves += " " + str(MoveNumber) + ". " + row
            MoveNumber += 1
        else:
            moves += " " + row
            WhiteMove = True

    moves = moves.strip()

    
    MovesCount = 1
    Set5  = Set10 = Set15 = Set20 = Set30 = Set40 = Set70 = Set_Remain = ""
    #Set 5 contruction
    # find 6. in moves string
    Find6th = moves.find(" 6.")
    Set5 = moves
    if(Find6th != -1):
        Set5 = moves[0:Find6th]

    #Set 10 contruction
    # find 11. in moves string
    Find11th = moves.find(" 11.")
    if(Find11th != -1):
        Set10 = moves[Find6th:Find11th]
        MovesCount = 2
    elif(Find6th != -1):
        Set10 = moves[Find6th:]
        MovesCount = 2

    #Set 15 contruction
    # find 16. in moves string
    Find16th = moves.find(" 16.")
    if(Find16th != -1):
      Set15 = moves[Find11th:Find16th]
      MovesCount = 3
    elif(Find11th != -1):
      Set15 = moves[Find11th:]
      MovesCount = 3

    #Set 20 contruction
    # find 21. in moves string
    Find21st = moves.find(" 21.")
    if(Find21st != -1):
      Set20 = moves[Find16th:Find21st]
      MovesCount = 4
    elif(Find16th != -1):
      Set20 = moves[Find16th:]
      MovesCount = 4

    #Set 30 contruction
    # find 31. in moves string
    Find31st = moves.find(" 31.")
    if(Find31st != -1):
      Set30 = moves[Find21st:Find31st]
      MovesCount = 5
    elif(Find21st != -1):
      Set30 = moves[Find21st:]
      MovesCount = 5

    #Set 40 contruction
    # find 41. in moves string
    Find41st = moves.find(" 41.")
    if(Find41st != -1):
      Set40 = moves[Find31st:Find41st]
      MovesCount = 6
    elif(Find31st != -1):
      Set40 = moves[Find31st:]
      MovesCount = 6

    #Set 70 contruction
    # find 71. in moves string
    Find71st = moves.find(" 71.")
    if(Find71st != -1):
      Set70 = moves[Find41st:Find71st]
      MovesCount = 7
    elif(Find41st != -1):
      Set70 = moves[Find41st:]
      MovesCount = 7

    #Set 70 contruction
    if(Find71st != -1):
      Set_Remain = moves[Find71st:]
      MovesCount = 8

    successbit = True
    move_array = [MovesCount,Set5.strip(),Set10.strip(),Set15.strip(),Set20.strip(),Set30.strip(),Set40.strip(),Set70.strip(),Set_Remain.strip()]

  
    return move_array,successbit


def pgn_to_coordinates(pgn_text):
    # Use StringIO to treat the string like a file
    pgn_file = io.StringIO(pgn_text)
    
    # Read the game from the PGN
    game = chess.pgn.read_game(pgn_file)
    if not game:
        return []

    coordinate_moves = []
    
    # Iterate through the main line of the game
    for move in game.mainline_moves():
        # .uci() returns the move in Pure Coordinate format (e.g., 'g1f3')
        coordinate_moves.append(move.uci())

    return coordinate_moves

