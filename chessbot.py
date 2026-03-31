#import mysql.connector
#from mysql.connector import Error
ConnectString = "mysql -h database-1.cfvrvxxcdsku.ca-west-1.rds.amazonaws.com -P 3306 -u admin -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=./global-bundle.pem"

host=ConnectString[9:60]
user='admin'
password='Data608-Project'
database='CHESSBOT'

#---------------------------------------

import warnings

# Suppress the specific Google Generative AI warning
warnings.filterwarnings("ignore")

import nextmove as nm
import metrics as mt
import movelist as ml
import boardImage as bI
import htmlPagetemplate as ht
import nextmove as nm
import snark as sn
import re
import mysql.connector
from mysql.connector import Error
from datetime import datetime

#---------------------------------------
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    #define blank variables for initial State 0 of website
    HiddenInputs = ""
    SourceSpaceColoum = ""
    SourceSpaceRow = ""
    DestinationSpaceColoum = ""
    DestinationSpaceRow = ""
    AllMovesString = ""
    BotDifficulty = ""
    MetricDisplay = "0"
    SnarkLevel = ""
    RemarkFreq = ""
    RemarkType = "general_move"
    RemarkText = ""
    GameCondition = "start"
    BoardRow1 = "r,n,b,q,k,b,n,r";    #row 1 a through h
    BoardRow2 = "p,p,p,p,p,p,p,p";
    BoardRow3 = "0,0,0,0,0,0,0,0";
    BoardRow4 = "0,0,0,0,0,0,0,0";
    BoardRow5 = "0,0,0,0,0,0,0,0";
    BoardRow6 = "0,0,0,0,0,0,0,0";
    BoardRow7 = "P,P,P,P,P,P,P,P";
    BoardRow8 = "R,N,B,Q,K,B,N,R";   # row 8  a through h

    #Boardlayout is 8x8 array (where BoardLayout[x][y] is addressing  (row x+1) (column y+1))
    BoardLayout = [BoardRow1.split(","),BoardRow2.split(","),BoardRow3.split(","),BoardRow4.split(","),BoardRow5.split(","),BoardRow6.split(","),BoardRow7.split(","),BoardRow8.split(",")]


    
    
    #check if POST variables are available,  for state N of website
    if request.method == 'POST' and request.form.get('action') != 'reset':
        # Capture data from the form input named 'content'
        SourceSpaceColoum = request.form.get('SourceSpaceColoum')
        SourceSpaceRow = request.form.get('SourceSpaceRow')
        DestinationSpaceColoum = request.form.get('DestinationSpaceColoum')
        DestinationSpaceRow = request.form.get('DestinationSpaceRow')
        AllMovesString = request.form.get('AllMovesString')
        BotDifficulty = request.form.get('BotDifficulty')
        MetricDisplay = request.form.get('MetricDisplay')
        SnarkLevel = request.form.get('SnarkLevel')
        RemarkFreq = request.form.get('RemarkFreq')
        GameCondition = request.form.get('GameCondition')
    
        UserMove = SourceSpaceColoum +  SourceSpaceRow +  DestinationSpaceColoum + DestinationSpaceRow

        #connect to database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database='CHESSBOT' # Optional: leave out to create DB first
           )
        
        if connection.is_connected():
            cursor = connection.cursor()
        else:
            exit()
        
        BotMove,Metrics,BoardLayout,GameCondition = nm.nextmove(BoardLayout,AllMovesString,UserMove,cursor,BotDifficulty,GameCondition)
        
        # append AllMovesString with new pair of moves
        move_numbers = 1
        if not AllMovesString:
                AllMovesString = f"{move_numbers}. {UserMove} {BotMove}"
        else:
            move_numbers = len(re.findall(r'\d+\.', AllMovesString))
            move_numbers += 1
            AllMovesString += f" {move_numbers}. {UserMove} {BotMove}"

        #call snark remark
        should_remark = move_numbers % int(RemarkFreq)

        if SnarkLevel != "off" and GameCondition == "middle" and should_remark == 0:
                RemarkText = sn.snark(RemarkType,SnarkLevel,move_numbers)
        elif "end" in GameCondition and SnarkLevel != "off": 
                RemarkText = sn.snark(GameCondition,SnarkLevel,move_numbers)
        elif "end" in GameCondition:
                if(GameCondition == "Bend"):
                    RemarkText = "Game Ends with Black Checkmate"
                elif(GameCondition == "Wend"):
                    RemarkText = "Game Ends with White Checkmate"
                else:
                    RemarkText = "Game Ends with unique position"

            
        #--------------------------------------- (build hidden variables)
        
        HiddenInputs = '<input type="hidden" name="AllMovesString" value="' + AllMovesString +'">'
        HiddenInputs += '<input type="hidden" name="BotDifficulty" value="' + BotDifficulty +'">'
        HiddenInputs += '<input type="hidden" name="MetricDisplay" value="' + MetricDisplay +'">'
        HiddenInputs += '<input type="hidden" name="SnarkLevel" value="' + SnarkLevel +'">'
        HiddenInputs += '<input type="hidden" name="RemarkFreq" value="' + RemarkFreq +'">'
        HiddenInputs += '<input type="hidden" name="GameCondition" value="' + GameCondition +'">'
    
    #call outside-----------------------
    #obtain webpage base template
    FirstPartOfPage = ht.htmlPagetemplate(1)
    SecondPartOfPage = ht.htmlPagetemplate(2)
    SecondSecondPartOfPage = ht.htmlPagetemplate(25)
    if GameCondition and "end" not in GameCondition:
        metric_val = Metrics[2][0][0] if 'Metrics' in locals() or 'Metrics' in globals() else "    "
    else:
        metric_val = "    " 

    FourthPartOfPage = ht.htmlPagetemplate(4)
    FifthPartOfPage = ht.htmlPagetemplate(5)

    if GameCondition and "end" in GameCondition:
        ThirdPartOfPage = ht.htmlPagetemplate(8)
    else: 
        ThirdPartOfPage = ht.htmlPagetemplate(3,metric_val)
    
    #---------------------------------------

    #call boardimage ~ 64 times
    for row in range(8, 0, -1):  # Corrected: start at 8, stop at 1, step -1
        FirstPartOfPage += '<tr><td>' + str(row) + "</td>"
        for column in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            space_address = f"{column}{row}" 
    
            # Call your boardImage function
            PiecePictureName = bI.boardImage(BoardLayout, space_address)
            
            # Debug print
    #        print(f"{space_address} -> {PiecePictureName}")
    
            FirstPartOfPage += f'<td><img src="https://raw.githubusercontent.com/Sundeep-Parmar-UC/608-project-ver1/refs/heads/main/{PiecePictureName}" width="65" alt="Chess Square {space_address}"></td>'
        FirstPartOfPage += '</tr>'
    
    FirstPartOfPage += '<tr><td></td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td><td>H</td></tr>'
                  
    #---------------------------------------
            
    #call movelist
    BaseMovesList = ml.movelist(AllMovesString)
    
    for row in BaseMovesList:
        SecondPartOfPage += '<tr>'
        SecondPartOfPage += '<td style="padding: 6px; border: 2px solid #ddd; font-weight: bold;">'
        SecondPartOfPage += str(row[0])
        SecondPartOfPage += '</td><td style="padding: 6px; border: 2px solid #ddd;">'
        SecondPartOfPage += row[1]
        SecondPartOfPage += '</td><td style="padding: 6px; border: 2px solid #ddd;">'
        SecondPartOfPage += row[2]    
        SecondPartOfPage += '</td>'
        SecondPartOfPage += '</tr>'
    
    #added Metric option  or display Metrics
    MetricDecision = ""
    if MetricDisplay == "0" and len(AllMovesString) == 0:
        #added questionaire for metrics
        MetricDecision = '<tr><td colspan="2" style="border: 2px solid #555;">Display Metrics:<br><BIG><input type="radio" id="on" name="MetricDisplay" value="1"><label for="on">On</label>'
        MetricDecision += '<input type="radio" id="off" name="MetricDisplay" value="0" checked><label for="off">Off</label></BIG>'
        MetricDecision += '</td><td style="border: 2px solid #555;">Bot Difficulty: <br><select id="BotDiff" name="BotDifficulty" style="font-size: 24px; padding-left: 20px; padding-right: 20px;">'
        MetricDecision += '<option value="1000">Easy</option><option value="1500" selected>Medium</option><option value="2500">Hard</option><option value="5000">Grand Master</option></select>'
        
        MetricDecision += '</td><td style="border: 2px solid #555;">Bot Response Style:<br><select id="Snark" name="SnarkLevel" style="font-size: 24px; padding-left: 20px; padding-right: 20px;">'
        MetricDecision += '<option value="off" checked>Off</option><option value="neutral" disabled>Neutral</option><option value="positive" disabled>Encouraging</option><option value="evil" disabled>Snob</option></select>'
    
        MetricDecision += '</td><td colspan="2" style="border: 2px solid #555;">Bot Response Frequency:<br><select id="Freq" name="RemarkFreq" style="font-size: 24px; padding-left: 20px; padding-right: 20px;">'
        MetricDecision += '<option value="10">Low</option><option value="4" selected>Medium</option><option value="1">High</option></select>'
        
        MetricDecision += '</td></tr>'
    
    elif MetricDisplay == "1" and Metrics:
        #display metrics
        MetricDecision = f'<tr><td colspan="2" style="border: 2px solid #555;">Number of games considered: {Metrics[0]}</td>'
        MetricDecision += '<td colspan="3" style="border: 2px solid #555;">Bot Moves considered:<br>'
        for row in Metrics[1]:
            MetricDecision += f'Move: {row[0]} >> {row[1]*100:.2f}%<br>'
        
        MetricDecision += '</td><td colspan="2" style="border: 2px solid #555;">Next move for user:<br>'
        
        for row in Metrics[2]:
            MetricDecision += f'Move: {row[0]} # of games: {row[1]}<br>'

        MetricDecision += '</td></tr>'
        for row in Metrics[3]:
            MetricDecision += f'<tr><td colspan="2" style="border: 2px solid #555;">File: {row[0]} </td><td colspan="2" style="border: 2px solid #555;"> Total Games: {row[1]} </td><td colspan="2" style="border: 2px solid #555;"> Ingest Games : {row[2]} </td><td style="border: 2px solid #555;"> File Size: {row[3]} </td></tr>'

    elif "end" in GameCondition and Metrics:
        for row in Metrics[3]:
            MetricDecision += f'<tr><td colspan="2" style="border: 2px solid #555;">File: {row[0]} </td><td colspan="2" style="border: 2px solid #555;"> Total Games: {row[1]} </td><td colspan="2" style="border: 2px solid #555;"> Ingest Games : {row[2]} </td><td style="border: 2px solid #555;"> File Size: {row[3]} </td></tr>'
    
    FourthPartOfPage = HiddenInputs + MetricDecision + FourthPartOfPage

    #---------------------------------------

    SecondSecondPartOfPage = SecondSecondPartOfPage + '<p style="color: white; font-style: italic;font-size: 24px;">' + RemarkText + '</p><br>'
    
    #output webpage raw
    BuildPage = FirstPartOfPage + SecondPartOfPage + SecondSecondPartOfPage + ThirdPartOfPage + FourthPartOfPage + FifthPartOfPage
    
    return BuildPage

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)
