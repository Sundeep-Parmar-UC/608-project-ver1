#import mysql.connector
#from mysql.connector import Error
ConnectString = "mysql -h database-1.clqxqhhe6wft.us-east-1.rds.amazonaws.com -P 3306 -u admin -p'<Enter_DB_Password>' --ssl-verify-server-cert  --ssl-ca=/certs/global-bundle.pem mysql"

host=ConnectString[9:60]
user='admin'
password='Data608-Project'
database='CHESSBOT'

Logging = ""
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
    MetricDisplay = ""
    SnarkLevel = ""
    RemarkFreq = ""
    RemarkType = ""
    RemarkText = ""
    GameCondition = ""
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
    if request.method == 'POST':
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
        RemarkType = request.form.get('RemarkType')
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
            Logging += "MYSQL Connection Failed"
            exit()
        
        BotMove,Metrics,BoardLayout,GameCondition = nm.nextmove(BoardLayout,AllMovesString,UserMove,cursor,BotDifficulty,GameCondition)
        
        Logging += "GameCondition: " + GameCondition
        
        # append AllMovesString with new pair of moves
        move_numbers = re.findall(r'(\d+)\.', AllMovesString)
        next_num = int(move_numbers[-1]) + 1 if move_numbers else 1
        AllMovesString += f" {next_num}. {UserMove} {BotMove}"

        Logging += "AllMovesString: " + AllMovesString

        #call snark remark
        if(GameCondition == "middle"):
            RemarkText = sn.snark(RemarkType,SnarkLevel,len(BaseMovesList))
        else:
            RemarkText = sn.snark(GameCondition,SnarkLevel,len(BaseMovesList))

        #--------------------------------------- (build hidden variables)
        
        HiddenInputs = '<input type="hidden" name="AllMovesString" value="' + AllMovesString +'">'
        HiddenInputs += '<input type="hidden" name="BotDifficulty" value="' + BotDifficulty +'">'
        HiddenInputs += '<input type="hidden" name="MetricDisplay" value="' + MetricDisplay +'">'
        HiddenInputs += '<input type="hidden" name="SnarkLevel" value="' + SnarkLevel +'">'
        HiddenInputs += '<input type="hidden" name="RemarkFreq" value="' + RemarkFreq +'">'
        HiddenInputs += '<input type="hidden" name="RemarkType" value="' + RemarkType +'">'
        HiddenInputs += '<input type="hidden" name="GameCondition" value="' + GameCondition +'">'
    
    #call outside-----------------------
    #obtain webpage base template
    FirstPartOfPage = ht.htmlPagetemplate(1)
    SecondPartOfPage = ht.htmlPagetemplate(2)
    ThirdPartOfPage = ht.htmlPagetemplate(3)
    FourthPartOfPage = ht.htmlPagetemplate(4)
    FifthPartOfPage = ht.htmlPagetemplate(5)
    
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
    
            FirstPartOfPage += f'<td><img src="https://raw.githubusercontent.com/Sundeep-Parmar-UC/608-project-ver1/refs/heads/main/{PiecePictureName}" width="100" alt="Chess Square {space_address}"></td>'
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
        MetricDecision = '<tr><td colspan="2" style="border: 2px solid #555;">Display Metrics:<br><BIG><input type="radio" id="on" name="MetricDisplay" value="1" checked><label for="on">On</label>'
        MetricDecision += '<input type="radio" id="off" name="MetricDisplay" value="0"><label for="off">Off</label></BIG>'
        MetricDecision += '</td><td style="border: 2px solid #555;">Bot Difficulty: <br><select id="BotDiff" name="BotDifficulty" style="font-size: 34px; padding-left: 20px; padding-right: 20px;">'
        MetricDecision += '<option value="1000">Easy</option><option value="1500" selected>Medium</option><option value="2500">Hard</option><option value="5000">Grand Master</option></select>'
        
        MetricDecision += '</td><td style="border: 2px solid #555;">Bot Response Style:<br><select id="Snark" name="SnarkLevel" style="font-size: 34px; padding-left: 20px; padding-right: 20px;">'
        MetricDecision += '<option value="off">Off</option><option value="neutral" selected>Neutral</option><option value="positive">Encouraging</option><option value="evil">Snob</option></select>'
    
        MetricDecision += '</td><td colspan="2" style="border: 2px solid #555;">Bot Response Frequency:<br><select id="Freq" name="RemarkFreq" style="font-size: 34px; padding-left: 20px; padding-right: 20px;">'
        MetricDecision += '<option value="10">Low</option><option value="4" selected>Medium</option><option value="1">High</option></select>'
        
        MetricDecision += '</td></tr>'
    
    elif MetricDisplay == "1":
        #display metrics
        MetricDecision = f'<tr><td colspan="2" style="border: 2px solid #555;">Number of games considered: {Metrics[0]}</td>'
        MetricDecision += '<td colspan="2" style="border: 2px solid #555;">Bot Moves considered:<br>'
        for row in Metrics[1]:
            MetricDecision += f'Move: {row[0]} >> {row[1]*100:.2f}%<br>'
        
        MetricDecision += '</td><td colspan="2" style="border: 2px solid #555;">Next move for user:<br>'
        
        for row in Metrics[2]:
            MetricDecision += f'Move: {row[0]} # of games: {row[1]}<br>'
        
        MetricDecision += '</td></tr>'
    
    FourthPartOfPage = HiddenInputs + MetricDecision + FourthPartOfPage

    #---------------------------------------
    
    FifthPartOfPage = RemarkText + FifthPartOfPage
    
    #output webpage raw
    BuildPage = FirstPartOfPage + SecondPartOfPage + ThirdPartOfPage + FourthPartOfPage + FifthPartOfPage
    
    return BuildPage

if __name__ == '__main__':
    app.run(debug=True)
