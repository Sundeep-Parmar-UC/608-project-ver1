#    Construct SQL statement
#    WhiteELO, BlackELO, Opening, Site, Termination, 
#    Insert game data using SQL connector
#    Obtain Game_ID from SQL connector
#    Return [game_id],[successbit] (true)

def LoadGame(game_data,SQLconnect):

    GameSQL = "INSERT INTO games (Site,White_ELO, Black_ELO, Opening) VALUES (%s, %s, %s, %s)"
#    successbit += f"#SQLconnect.execute({GameSQL}, ({game_data[0]}, {game_data[1]}, {game_data[2]}, {game_data[3]}))" + "<br>"

    SQLconnect.execute(GameSQL, (game_data[0], game_data[1], game_data[2], game_data[3]))
    InsertedRecord = SQLconnect.lastrowid
    successbit = f"Record inserted. game_ID: {InsertedRecord} <br>"

    return InsertedRecord,successbit
