#    Construct SQL statement
#    WhiteELO, BlackELO, Opening, Site, Termination, 
#    Insert game data using SQL connector
#    Obtain Game_ID from SQL connector
#    Return [game_id],[successbit] (true)

def LoadGame(game_data,SQLconnect):

    successbit = ""
    GameSQL = "INSERT INTO games (White_ELO, Black_ELO, Opening, Site, Termination) VALUES (%s, %s, %s, %s, %s)"
    successbit += f"#SQLconnect.execute({GameSQL}, ({game_data[0]}, {game_data[1]}, {game_data[2]}, {game_data[3]}, {game_data[4]}))" + "<br>"

    #Retrieve the last inserted ID
    #game_id = SQLconnect.lastrowid  # This gets the 'ID' automatically
    
    game_id = 100
 
    return game_id,successbit
