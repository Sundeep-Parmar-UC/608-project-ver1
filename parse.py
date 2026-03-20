import loadgame as lg
import parsemove as pm
import loadmove as lm
import re
import mysql.connector


def Parse(uncompressFilePath,SQLconnect):

    #Set variable to stop collecting events after # lines read
    Stop_loading_data_after_lines = 5000000
    
    # Define the desired column names: WhiteELO, BlackELO, Opening, Site, Termination, 

    EventArray = ['Site','WhiteElo','BlackElo','Opening','Termination','Moves']
    ## create chess games data frame
    LinesTotalRead = 0 #line number of input data
    MoveLineGathered = False # indicator of last event element collected
    Eventscollected = 0 #number of events collected
    Eventsskipped = 0 #number of events skipped
    Log = ""
    # Download the file from the URL and save it locally
    #urllib.request.urlretrieve(file_url, local_filename)
    #print(f"File '{local_filename}' downloaded successfully from '{file_url}'.")

    #open local copy of the data set
    with open(uncompressFilePath, 'r') as file:
        while True:
            if LinesTotalRead == Stop_loading_data_after_lines:
              Log += "Data collection stopped at line: "+str(Stop_loading_data_after_lines) + "<br>"
              break

            line = file.readline() #read one line from data file
            LinesTotalRead+=1 # increment lines read
            if LinesTotalRead % 10000 == 0:
                print("LinesTotalRead: ",LinesTotalRead)
            
            if not line:  # Check if the line is an empty string, indicating EOF
                Log += "End of file reached." # stop processing, all events should have been saved.
                break
            elif line.startswith('[Site '): #Found Site info
                SiteData = line[7:(8+line[8:].find("\""))]
            elif line.startswith('[WhiteElo '): #Found WhiteElo info
                WhiteEloData = line[11:(12+line[12:].find("\""))]
            elif line.startswith('[BlackElo '): #Found BlackElo info
                BlackEloData = line[11:(12+line[12:].find("\""))]
            elif line.startswith('[Opening '): #Found Opening info
                OpeningData = line[10:(11+line[11:].find("\""))]
            elif line.startswith('[Termination '): #Found Termination info
                TerminationData = line[14:(15+line[15:].find("\""))]
            elif line.startswith('1. '): #Found Moves info
                MovesData = line.strip() # Use the entire line for the Moves column    

                if MoveValidation(MovesData):
                    MoveLineGathered = True  #found game with natural checkmate
#                   Log += "Found Natural Checkmate game:<br>"
                else:
#                   Log += "Not natural checkmate :<br>"
                    Eventsskipped+=1

                #All data for single event has been obtained. Store in main data frame
                if (MoveLineGathered):
                    MoveLineGathered = False
                    #contruct GameData
                    #EventArray = ['Site','WhiteElo','BlackElo','Opening','Moves']
                    CollectedEvent = [SiteData,WhiteEloData,BlackEloData,OpeningData]
                    game_id_returned,success_bit = lg.LoadGame(CollectedEvent,SQLconnect)
#                    Log += "game_id_returned: " + str(game_id_returned) + "<br>"
#                    Log += "success_bit: " + str(success_bit) + "<br>"

                    move_array,success_move_bit = pm.ParserMove(MovesData)
#                    Log += "MovedCount:" + str(move_array[0]) + "<br>"
#                    Log += "Set5:" + move_array[1] + "<br>"
#                    Log += "Set10:" + move_array[2] + "<br>"
#                    Log += "Set15:" + move_array[3] + "<br>"
#                    Log += "Set20:" + move_array[4] + "<br>"
#                    Log += "Set30:" + move_array[5] + "<br>"
#                    Log += "Set40:" + move_array[6] + "<br>"
#                    Log += "Set70:" + move_array[7] + "<br>"
#                    Log += "Set_Remain:" + move_array[8] + "<br>"
#                    Log += "success_move_bit: " + str(success_move_bit) + "<br>"

                    Complete_bit = lm.LoadMove(move_array,move_array[0],BlackEloData,game_id_returned,SQLconnect)
#                    Log += "Complete_bit: " + str(Complete_bit) + "<br>"                    
                    Eventscollected+=1
    
                    
                SiteData = WhiteEloData = BlackEloData = OpeningData = TerminationData = MovesData = ''

    Log += "File Parse ended <br>"
    
    metric = [Eventscollected,Eventsskipped,Log,"Game","Moves",uncompressFilePath]
    successbit = True
    return metric,successbit



def MoveValidation(moves):
    ApprovedMoves = False

    if re.search(r"# [01]-[01]$", moves):
        ApprovedMoves = True
    
    if "=" in moves:
        ApprovedMoves = False

    return ApprovedMoves