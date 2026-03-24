# receive board layout
# receive Moves String
# receive user move
# receive SQL connector
# receive BotDifficulty
# receive GameCondition

# construction user move with Moves string
# prepare SQL statement
# obtain list of all next moves
#build metric
#decide next move
#call baord update function

#return next botmove, metricarray, board layout


import board as bd
import re
from collections import Counter

def nextmove(BoardLayout,MovesString,UserMove,SQLconnect,BotDifficulty,GameCondition):

    # construction user move with Moves string
    #count number of moves in
    move_pairs = len(re.findall(r'\d+\.', MovesString))
    move_pairs += 1
    MovesString = MovesString + " " + str(move_pairs) + ". " + UserMove
#    print(MovesString) 
    
    # prepare SQL statement
    SQLStatementEnd = ""    
    Set5  = Set10 = Set15 = Set20 = Set30 = Set40 = Set70 = Set_Remain = ""
    #Set 5 contruction
    # find 6. in moves string
    Find6th = MovesString.find(" 6.")
    Set5 = MovesString
    
    if(Find6th != -1):
        Set5 = MovesString[0:Find6th].strip()
        SQLStatementEnd += "Set5 = '" + Set5 + "' "
    else:
        Set5 = MovesString
        SQLStatementEnd += "Set5 LIKE '" + Set5 + "%' "

    #Set 10 contruction
    # find 11. in moves string
    Find11th = MovesString.find(" 11.")
    if(Find11th != -1):
        Set10 = MovesString[Find6th:Find11th].strip()
        SQLStatementEnd += "AND Set10 = '" + Set10 + "' "
    elif(Find6th != -1):
        Set10 = MovesString[Find6th:].strip()
        SQLStatementEnd += "AND Set10 LIKE '" + Set10 + "%' "

    #Set 15 contruction
    # find 16. in moves string
    Find16th = MovesString.find(" 16.")
    if(Find16th != -1):
        Set15 = MovesString[Find11th:Find16th].strip()
        SQLStatementEnd += "AND Set15 = '" + Set15 + "' "
    elif(Find11th != -1):
        Set15 = MovesString[Find11th:].strip()
        SQLStatementEnd += "AND Set15 LIKE '" + Set15 + "%' "

    #Set 20 contruction
    # find 21. in moves string
    Find21st = MovesString.find(" 21.")
    if(Find21st != -1):
        Set20 = MovesString[Find16th:Find21st].strip()
        SQLStatementEnd += "AND Set20 = '" + Set20 + "' "
    elif(Find16th != -1):
        Set20 = MovesString[Find16th:].strip()
        SQLStatementEnd += "AND Set20 LIKE '" + Set20 + "%' "

    #Set 30 contruction
    # find 31. in moves string
    Find31st = MovesString.find(" 31.")
    if(Find31st != -1):
        Set30 = MovesString[Find21st:Find31st].strip()
        SQLStatementEnd += "AND Set30 = '" + Set30 + "' "
    elif(Find21st != -1):
        Set30 = MovesString[Find21st:].strip()
        SQLStatementEnd += "AND Set30 LIKE '" + Set30 + "%' "

    #Set 40 contruction
    # find 41. in moves string
    Find41st = MovesString.find(" 41.")
    if(Find41st != -1):
        Set40 = MovesString[Find31st:Find41st].strip()
        SQLStatementEnd += "AND Set40 = '" + Set40 + "' "
    elif(Find31st != -1):
        Set40 = MovesString[Find31st:].strip()
        SQLStatementEnd += "AND Set40 LIKE '" + Set40 + "%' "

    #Set 70 contruction
    # find 71. in moves string
    Find71st = MovesString.find(" 71.")
    if(Find71st != -1):
        Set70 = MovesString[Find41st:Find71st].strip()
        SQLStatementEnd += "AND Set70 = '" + Set70 + "' "
    elif(Find41st != -1):
        Set70 = MovesString[Find41st:].strip()
        SQLStatementEnd += "AND Set70 LIKE '" + Set70 + "%' "

    #Set 70 contruction
    if(Find71st != -1):
        Set_Remain = MovesString[Find71st:].strip()
        SQLStatementEnd += "AND Set_Remain LIKE '" + Set_Remain + "%' "

#    SQLQuery = "SELECT * FROM moves WHERE BlackELO <= " + BotDifficulty + " " + SQLStatementEnd
    SQLQuery = "SELECT * FROM moves WHERE  " + SQLStatementEnd
     
    print(SQLQuery)    

    # obtain list of all next moves
    SQLconnect.execute(SQLQuery)
    records = SQLconnect.fetchall()
    #Order received: 0-id, 1-Set5, 2-Set10, 3-Set15, 4-Set20, 5-Set30, 6-Set40, 7-Set70, 8-Set_Remain, 9-BlackELO, 10-Game_id
    

    #build metric
    # num of games to consider
    NumofGames = len(records)
    print(f"Total Games found: {len(records)}")
    AllPossiblemoves = []
    if(NumofGames == 0):
        GameCondition = "Uend" 
    else:
        GameCondition = "middle"         
        #decide next move
        BotMovestoConsider = []
    
        for i in range(NumofGames):
            Possiblemoves = " ".join(str(records[i][j]) for j in range(1, 9) if records[i][j] is not None)
            if move_pairs < 6:
                # Added .strip() to clean up leading spaces
                raw_move = records[i][1].removeprefix(Set5)
                Possiblemoves = Possiblemoves.removeprefix(Set5)
            elif move_pairs < 11:
                raw_move = records[i][2].removeprefix(Set10)
                Possiblemoves = Possiblemoves.removeprefix(Set10)
            elif move_pairs < 16:
                raw_move = records[i][3].removeprefix(Set15)
                Possiblemoves = Possiblemoves.removeprefix(Set15)
            elif move_pairs < 21:
                raw_move = records[i][4].removeprefix(Set20)
                Possiblemoves = Possiblemoves.removeprefix(Set20)
            elif move_pairs < 31:
                raw_move = records[i][5].removeprefix(Set30)
                Possiblemoves = Possiblemoves.removeprefix(Set30)
            elif move_pairs < 41:
                raw_move = records[i][6].removeprefix(Set40)
                Possiblemoves = Possiblemoves.removeprefix(Set40)
            elif move_pairs < 71:
                raw_move = records[i][7].removeprefix(Set70)
                Possiblemoves = Possiblemoves.removeprefix(Set70)
            else:
                raw_move = records[i][8].removeprefix(Set_Remain) # Fixed variable name
                Possiblemoves = Possiblemoves.removeprefix(Set_Remain)

            # Clean up and append
            BotMovestoConsider.append(raw_move.strip()[0:4])

            #build long string for all games and then grab N+1 moves possible
            AllPossiblemoves.append(Possiblemoves.strip())

        # 1. Get histogram of all next moves
        move_counts = Counter(BotMovestoConsider)
        
        # 2. Collect next moves into metric array with percentage
        MovesConsideredMetric = []
        for move, count in move_counts.most_common():
            MovesConsideredMetric.append([move,round(count/NumofGames, 3)])
    
        #select highest percentage move as bot move
        BotMove = MovesConsideredMetric[0][0].strip()
        print("selected BotMove: ",BotMove)
        
        if(BotMove == ""):
            GameCondition = "Wend" 

        NextPossibleMove = []
        for NextMoveRow in AllPossiblemoves:
            if(NextMoveRow[0:4].strip() == BotMove):
                NextPossibleMove.append(NextMoveRow[NextMoveRow.find(".")+2:NextMoveRow.find(".")+6])

        # 1. Get histogram of all next moves
        Possiblemove_counts = Counter(NextPossibleMove)
        
        # 2. Collect next moves into metric array with percentage
        PossibleMovesConsideredMetric = []
        for move2, count2 in Possiblemove_counts.most_common():
            PossibleMovesConsideredMetric.append([move2,count2])
        
  
        Metrics = [NumofGames,MovesConsideredMetric,PossibleMovesConsideredMetric]


        #call baord update function  
    #    print("calling board update")
    
    
        #1. split input  PGN-style MovesString into tokens
        tokens = MovesString.split()
        
        #2. Skip move numbers "1.", "2." etc.
        moves = [t for t in tokens if not t.endswith(".")]
    
        #3. Build movelist html-ready MoveTable
        MoveTable = []
        for idx, move in enumerate(moves):
            BoardLayout = bd.board(move, BoardLayout)
    #        print(f"BoardLayout = bd.board(UserMove, BoardLayout): BoardLayout = bd.board({move}, BoardLayout")
    #        for i in range(8):
    #            print(BoardLayout[i])
    
    #    print(f"BoardLayout = bd.board(UserMove, BoardLayout): BoardLayout = bd.board({BotMove}, BoardLayout")
        BoardLayout = bd.board(BotMove, BoardLayout)
        
    #    print("done board update")
    
    #    print("BotMove: ",BotMove)
        print("Metrics: ",Metrics)
    #    print("BoardLayout: ",BoardLayout)

    return BotMove,Metrics,BoardLayout,GameCondition