def LoadMove(move_array,num_moves,Black_ELO,game_id,SQLconnect):
    successbit = True
    MovesSQL = ""
    if(num_moves == 1):
        MovesSQL = "INSERT INTO moves (Set5, BlackELO, Game_id) VALUES (%s, %s, %s)"
#        successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]}, {Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1], Black_ELO, game_id))
#        successbit += "SQL insertation <br>"

    elif(num_moves == 2):
        MovesSQL = "INSERT INTO moves (Set5, Set10, BlackELO, Game_id) VALUES (%s, %s, %s, %s)"
#        successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]},{move_array[2]},{Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1],move_array[2], Black_ELO, game_id))
#        successbit += "SQL insertation <br>"

    elif(num_moves == 3):
        MovesSQL = "INSERT INTO moves (Set5, Set10, Set15, BlackELO, Game_id) VALUES (%s, %s, %s, %s, %s)"
#        successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]},{move_array[2]},{move_array[3]},{Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1],move_array[2],move_array[3],Black_ELO, game_id))
#        successbit += "SQL insertation <br>"

    elif(num_moves == 4):
        MovesSQL = "INSERT INTO moves (Set5, Set10, Set15, Set20, BlackELO, Game_id) VALUES (%s, %s, %s, %s, %s, %s)"
#        successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]},{move_array[2]},{move_array[3]},{move_array[4]},{Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1],move_array[2],move_array[3],move_array[4],Black_ELO, game_id))
#        successbit += "SQL insertation <br>"

    elif(num_moves == 5):
        MovesSQL = "INSERT INTO moves (Set5, Set10, Set15, Set20, Set30, BlackELO, Game_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
 #       successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]},{move_array[2]},{move_array[3]},{move_array[4]},{move_array[5]}{Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1],move_array[2],move_array[3],move_array[4],move_array[5],Black_ELO, game_id))
#        successbit += "SQL insertation <br>"

    elif(num_moves == 6):
        MovesSQL = "INSERT INTO moves (Set5, Set10, Set15, Set20, Set30, Set40, BlackELO, Game_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#        successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]},{move_array[2]},{move_array[3]},{move_array[4]},{move_array[5]},{move_array[6]},{Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1],move_array[2],move_array[3],move_array[4],move_array[5],move_array[6],Black_ELO, game_id))
#        successbit += "SQL insertation <br>"

    elif(num_moves == 7):
        MovesSQL = "INSERT INTO moves (Set5, Set10, Set15, Set20, Set30, Set40, Set70, BlackELO, Game_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#        successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]},{move_array[2]},{move_array[3]},{move_array[4]},{move_array[5]},{move_array[6]},{move_array[7]},{Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1],move_array[2],move_array[3],move_array[4],move_array[5],move_array[6],move_array[7],Black_ELO, game_id))
#        successbit += "SQL insertation <br>"

    elif(num_moves == 8):
        MovesSQL = "INSERT INTO moves (Set5, Set10, Set15, Set20, Set30, Set40, Set70, Set_Remain, BlackELO, Game_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#        successbit += f"#SQLconnect.execute({MovesSQL}, ({move_array[1]},{move_array[2]},{move_array[3]},{move_array[4]},{move_array[5]},{move_array[6]},{move_array[7]},{move_array[8]},{Black_ELO}, {game_id}))" + "<br>"
        SQLconnect.execute(MovesSQL, (move_array[1],move_array[2],move_array[3],move_array[4],move_array[5],move_array[6],move_array[7],move_array[8], Black_ELO, game_id))
#        successbit += "SQL insertation <br>"
    
    else:
        successbit = False

    return successbit
