#	Breakdown moves string
#	Construct move_array
#		Set5, Set10, Set15,Set20,Set30,Set40,Set70,Set_Remain
#	Return [move_array] 

import re

def ParserMove(moves):

    moves = re.sub(r"\{ \[%eval \d\.\d\d\] \}", "", moves)
    moves = re.sub(r"\{ \[%clk \d\.\d\d\] \}", "", moves)
    moves = moves.replace("...", ".")
    
    # Use regex to extract moves and move counts
    #moves_Piece_array = re.findall(r'\d+\.\s+([^\s]+)\s+([^\s]+)', moves)

    MovesCount = 0
    Set5  = Set10 = Set15 = Set20 = Set30 = Set40 = Set70 = Set_Remain = ""
    #Set 5 contruction
    # find 6. in moves string
    Find6th = moves.find(" 6.")
    if(Find6th != -1):
        Set5 = moves[0:Find6th]
        MovesCount = 1
    #Set 10 contruction
    # find 11. in moves string
    Find11th = moves.find(" 11.")
    if(Find11th != -1):
        Set10 = moves[Find6th:Find11th]
        MovesCount = 2
    elif(Find6th != -1):
        Set10 = moves[Find6th:-3]
        MovesCount = 2

    #Set 15 contruction
    # find 16. in moves string
    Find16th = moves.find(" 16.")
    if(Find16th != -1):
      Set15 = moves[Find11th:Find16th]
      MovesCount = 3
    elif(Find11th != -1):
      Set15 = moves[Find11th:-3]
      MovesCount = 3

    #Set 20 contruction
    # find 21. in moves string
    Find21st = moves.find(" 21.")
    if(Find21st != -1):
      Set20 = moves[Find16th:Find21st]
      MovesCount = 4
    elif(Find16th != -1):
      Set20 = moves[Find16th:-3]
      MovesCount = 4

    #Set 30 contruction
    # find 31. in moves string
    Find31st = moves.find(" 31.")
    if(Find31st != -1):
      Set30 = moves[Find21st:Find31st]
      MovesCount = 5
    elif(Find21st != -1):
      Set30 = moves[Find21st:-3]
      MovesCount = 5

    #Set 40 contruction
    # find 41. in moves string
    Find41st = moves.find(" 41.")
    if(Find41st != -1):
      Set40 = moves[Find31st:Find41st]
      MovesCount = 6
    elif(Find31st != -1):
      Set40 = moves[Find31st:-3]
      MovesCount = 6

    #Set 70 contruction
    # find 71. in moves string
    Find71st = moves.find(" 71.")
    if(Find71st != -1):
      Set70 = moves[Find41st:Find71st]
      MovesCount = 7
    elif(Find41st != -1):
      Set70 = moves[Find41st:-3]
      MovesCount = 7

    #Set 70 contruction
    if(Find71st != -1):
      Set_Remain = moves[Find71st:-3]
      MovesCount = 8

    successbit = True
    move_array = [MovesCount,Set5.strip(),Set10.strip(),Set15.strip(),Set20.strip(),Set30.strip(),Set40.strip(),Set70.strip(),Set_Remain.strip()]
    return move_array,successbit
