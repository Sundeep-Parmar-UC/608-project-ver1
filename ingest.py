import mysql.connector
from mysql.connector import Error
ConnectString = "mysql -h database-1.clqxqhhe6wft.us-east-1.rds.amazonaws.com -P 3306 -u admin -p'<Enter_DB_Password>' "

host=ConnectString[9:60]
user='admin'
password='Data608-Project'
database='CHESSBOT'



import obtain as ob
import decompress as dc
import parse as pa
import cleanup as cu
from datetime import datetime


#The user selects a file (month/year) to load into the database. 
#App connects to Lichess and downloads the compressed Data file
#App decompresses the Data file on EBS storage
#App parses the Data file for each chess game
#If game matches load conditions, 
#Then parse the moves value to make database-ready
#Insert Game data  and obtain game_id
#Insert Moves data with game_id
#Repeat till the end of the file
#Clean up the EBS, downloaded files, and uncompressed file
#Send Metrics and Remaining Space to the user


from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    AppLog = ""
    fileNameSelected = ""
    if request.method == 'POST':
        # Capture data from the form input named 'content'
        fileNameSelected = request.form.get('datafile')

        start_time = datetime.now()
        AppLog += "####-------------------- Process Start: " + start_time.strftime('%M:%S.%f')
        AppLog += "<br>"   
    
        #-----------------------------  Obtain
        AppLog += "Starting Obtain: " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        EBSpath = "/data/"
    
        AppLog += "Input EBSpath: " + EBSpath + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"   
        AppLog += "Input fileName: " + fileNameSelected + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
    
        downloadFileLocation = ob.Obtain(EBSpath,fileNameSelected)
    
        AppLog += "Output downloadFileLocation: " + downloadFileLocation + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        AppLog += "Ending Obtain: " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>--------<br>"
    
        #-----------------------------  Decompress
        AppLog += "Starting Decompress: " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        fileName = downloadFileLocation
        
        AppLog += "Input fileName: " + fileName + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"   
    
        uncompressFilePath,successbit = dc.Decompress(fileName)
    
        AppLog += "Output uncompressFilePath: " + uncompressFilePath + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        AppLog += "Output successbit: " + str(successbit) + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        AppLog += "Ending Decompress: " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>--------<br>"
    
        #-------------------------------- Database Connect
        AppLog += "Attempting MySQL Server connection: " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        connection = mysql.connector.connect(host=host,user=user,password=password,database=database,autocommit=True) 

        if connection.is_connected():
            cursor = connection.cursor()
            AppLog += "Connected to MySQL Server: " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>--------<br>"       
            
            #-----------------------------  Parse
            AppLog += "Starting Parse: " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>"
            
            AppLog += "Input uncompressFilePath: " + uncompressFilePath + " : " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>"   
            
            metric,successbit = pa.Parse(uncompressFilePath,cursor)
            
            AppLog += "Output metric (Events Found): " + str(metric[0]) + " : " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>"
            AppLog += "Output metric (Events Skipped): " + str(metric[1]) + " : " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>"
            AppLog += "Output metric (Log): " + str(metric[2]) + " : " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>"
            AppLog += "Ending Parse: " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>--------<br>"
            #-----------------------------  End Parse
            
        else:
            AppLog += "FAILED MySQL Server connection: " + datetime.now().strftime('%M:%S.%f')
            AppLog += "<br>--------<br>"       
    
        #-----------------------------  Cleanup
        AppLog += "Starting Cleanup: " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        
        AppLog += "Input EBSpath: " + EBSpath + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"   
        AppLog += "Input fileName: " + fileName + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"   
        AppLog += "Input uncompressFilePath: " + uncompressFilePath + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"   
    
        storageRemain = cu.Cleanup(EBSpath,fileName,uncompressFilePath)
    
        AppLog += "Output storageRemain: " + str(storageRemain) + " : " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>"
        AppLog += "Ending Cleanup: " + datetime.now().strftime('%M:%S.%f')
        AppLog += "<br>--------<br>"
    
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        AppLog += "####-------------------- Process End: " + str(elapsed_time)
        AppLog += "<br>"   

    # Simple HTML with a form and a display area
    BuildPage = "<div style='font-size: 25px; background-color: black; color: white; width: 100%; text-align: center;'>"
    BuildPage += "<h1>Data Ingestion and Training<br> By: G5-Rita Group</h1>"
    BuildPage += '<form method="POST">'
    BuildPage += '<label for="datafile">choose a DataSet to ingest: </label><br>'
    BuildPage += '<select id="datafile1" name="datafile" style="font-family: \'Courier New\', Courier, monospace; font-size: 34px; padding-left: 20px; padding-right: 20px;">'
    BuildPage += '<option value="lichess_db_standard_rated_2013-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2013 - January |&nbsp;17.8 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 121,332  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2013 - February |&nbsp;18.2 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 123,961  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2013 - March |&nbsp;23.6 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 158,635  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2013 - April |&nbsp;23.3 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 157,871  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2013 - May |&nbsp;26.5 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 179,550  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2013 - June |&nbsp;32.9 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 224,679  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2013 - July |&nbsp;&nbsp;&nbsp;43 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 293,459  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2013 - August |&nbsp;47.7 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 325,525  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2013 - September |&nbsp;47.2 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 325,098  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2013 - October |&nbsp;62.7 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 411,039  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2013 - November |&nbsp;&nbsp;&nbsp;77 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 487,012  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2013-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2013 - December |&nbsp;91.8 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 578,262  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2014 - January |&nbsp;&nbsp;111 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 697,600  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2014 - February |&nbsp;&nbsp;113 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 692,394  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2014 - March |&nbsp;&nbsp;129 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 795,173  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2014 - April |&nbsp;&nbsp;137 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 810,463  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2014 - May |&nbsp;&nbsp;172 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 905,374  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2014 - June |&nbsp;&nbsp;182 MB |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 961,868  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2014 - July |&nbsp;&nbsp;200 MB |&nbsp;&nbsp;&nbsp; 1,048,440  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2014 - August |&nbsp;&nbsp;193 MB |&nbsp;&nbsp;&nbsp; 1,013,294  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2014 - September |&nbsp;&nbsp;179 MB |&nbsp;&nbsp;&nbsp; 1,000,056  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2014 - October |&nbsp;&nbsp;205 MB |&nbsp;&nbsp;&nbsp; 1,111,302  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2014 - November |&nbsp;&nbsp;228 MB |&nbsp;&nbsp;&nbsp; 1,209,291  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2014-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2014 - December |&nbsp;&nbsp;259 MB |&nbsp;&nbsp;&nbsp; 1,350,176  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2015 - January |&nbsp;&nbsp;286 MB |&nbsp;&nbsp;&nbsp; 1,497,237  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2015 - February |&nbsp;&nbsp;283 MB |&nbsp;&nbsp;&nbsp; 1,495,553  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2015 - March |&nbsp;&nbsp;324 MB |&nbsp;&nbsp;&nbsp; 1,742,733  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2015 - April |&nbsp;&nbsp;317 MB |&nbsp;&nbsp;&nbsp; 1,785,418  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2015 - May |&nbsp;&nbsp;392 MB |&nbsp;&nbsp;&nbsp; 2,137,557  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2015 - June |&nbsp;&nbsp;432 MB |&nbsp;&nbsp;&nbsp; 2,324,106  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2015 - July |&nbsp;&nbsp;483 MB |&nbsp;&nbsp;&nbsp; 2,455,141  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2015 - August |&nbsp;&nbsp;504 MB |&nbsp;&nbsp;&nbsp; 2,621,861  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2015 - September |&nbsp;&nbsp;547 MB |&nbsp;&nbsp;&nbsp; 2,844,677  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2015 - October |&nbsp;&nbsp;647 MB |&nbsp;&nbsp;&nbsp; 3,400,418  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2015 - November |&nbsp;&nbsp;667 MB |&nbsp;&nbsp;&nbsp; 3,595,776  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2015-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2015 - December |&nbsp;&nbsp;758 MB |&nbsp;&nbsp;&nbsp; 4,161,162  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2016 - January |&nbsp;&nbsp;872 MB |&nbsp;&nbsp;&nbsp; 4,770,357  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2016 - February |&nbsp;&nbsp;908 MB |&nbsp;&nbsp;&nbsp; 5,015,361  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2016 - March |&nbsp;1.04 GB |&nbsp;&nbsp;&nbsp; 5,801,234  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2016 - April |&nbsp;1.06 GB |&nbsp;&nbsp;&nbsp; 5,922,667  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2016 - May |&nbsp;1.11 GB |&nbsp;&nbsp;&nbsp; 6,225,957  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2016 - June |&nbsp;1.09 GB |&nbsp;&nbsp;&nbsp; 6,136,419  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2016 - July |&nbsp;1.12 GB |&nbsp;&nbsp;&nbsp; 6,275,933  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2016 - August |&nbsp;1.16 GB |&nbsp;&nbsp;&nbsp; 6,483,257  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2016 - September |&nbsp;1.21 GB |&nbsp;&nbsp;&nbsp; 6,813,113  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2016 - October |&nbsp;1.35 GB |&nbsp;&nbsp;&nbsp; 7,599,868  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2016 - November |&nbsp;1.44 GB |&nbsp;&nbsp;&nbsp; 8,021,509  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2016-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2016 - December |&nbsp;&nbsp;1.7 GB |&nbsp;&nbsp;&nbsp; 9,433,412  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2017 - January |&nbsp;&nbsp;1.9 GB |&nbsp;&nbsp; 10,680,708  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2017 - February |&nbsp;&nbsp;1.8 GB |&nbsp;&nbsp; 10,194,939  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2017 - March |&nbsp;2.17 GB |&nbsp;&nbsp; 11,346,745  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2017 - April |&nbsp;3.48 GB |&nbsp;&nbsp; 11,348,506  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2017 - May |&nbsp;3.59 GB |&nbsp;&nbsp; 11,693,919  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2017 - June |&nbsp;3.52 GB |&nbsp;&nbsp; 11,512,600  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2017 - July |&nbsp;3.69 GB |&nbsp;&nbsp; 12,080,314  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2017 - August |&nbsp;3.81 GB |&nbsp;&nbsp; 12,458,761  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2017 - September |&nbsp;3.83 GB |&nbsp;&nbsp; 12,564,109  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2017 - October |&nbsp;4.18 GB |&nbsp;&nbsp; 13,703,878  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2017 - November |&nbsp;4.36 GB |&nbsp;&nbsp; 14,306,375  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2017-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2017 - December |&nbsp;4.95 GB |&nbsp;&nbsp; 16,232,215  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2018 - January |&nbsp;5.47 GB |&nbsp;&nbsp; 17,945,784  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2018 - February |&nbsp;5.28 GB |&nbsp;&nbsp; 17,383,410  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2018 - March |&nbsp;6.57 GB |&nbsp;&nbsp; 20,059,178  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2018 - April |&nbsp;6.02 GB |&nbsp;&nbsp; 19,881,929  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2018 - May |&nbsp;6.46 GB |&nbsp;&nbsp; 21,442,600  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2018 - June |&nbsp;6.09 GB |&nbsp;&nbsp; 20,273,737  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2018 - July |&nbsp;6.34 GB |&nbsp;&nbsp; 21,070,917  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2018 - August |&nbsp;6.81 GB |&nbsp;&nbsp; 22,635,642  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2018 - September |&nbsp;6.84 GB |&nbsp;&nbsp; 22,971,939  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2018 - October |&nbsp;7.39 GB |&nbsp;&nbsp; 24,784,600  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2018 - November |&nbsp;7.81 GB |&nbsp;&nbsp; 26,136,657  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2018-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2018 - December |&nbsp;&nbsp;9.3 GB |&nbsp;&nbsp; 31,179,146  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2019 - January |&nbsp;10.1 GB |&nbsp;&nbsp; 33,886,899  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2019 - February |&nbsp;9.17 GB |&nbsp;&nbsp; 31,023,718  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2019 - March |&nbsp;10.3 GB |&nbsp;&nbsp; 34,869,171  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2019 - April |&nbsp;9.87 GB |&nbsp;&nbsp; 33,565,536  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2019 - May |&nbsp;10.3 GB |&nbsp;&nbsp; 35,236,588  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2019 - June |&nbsp;9.98 GB |&nbsp;&nbsp; 33,935,786  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2019 - July |&nbsp;10.5 GB |&nbsp;&nbsp; 35,728,182  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2019 - August |&nbsp;10.8 GB |&nbsp;&nbsp; 36,745,427  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2019 - September |&nbsp;10.9 GB |&nbsp;&nbsp; 36,996,010  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2019 - October |&nbsp;11.9 GB |&nbsp;&nbsp; 40,440,254  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2019 - November |&nbsp;11.8 GB |&nbsp;&nbsp; 40,357,832  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2019-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2019 - December |&nbsp;12.9 GB |&nbsp;&nbsp; 44,055,757  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2020 - January |&nbsp;13.7 GB |&nbsp;&nbsp; 46,800,709  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2020 - February |&nbsp;12.9 GB |&nbsp;&nbsp; 44,004,185  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2020 - March |&nbsp;16.6 GB |&nbsp;&nbsp; 55,544,817  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2020 - April |&nbsp;22.2 GB |&nbsp;&nbsp; 73,224,608  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2020 - May |&nbsp;22.8 GB |&nbsp;&nbsp; 75,628,855  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2020 - June |&nbsp;21.1 GB |&nbsp;&nbsp; 70,374,749  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2020 - July |&nbsp;21.1 GB |&nbsp;&nbsp; 70,592,022  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2020 - August |&nbsp;21.2 GB |&nbsp;&nbsp; 71,405,167  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2020 - September |&nbsp;20.1 GB |&nbsp;&nbsp; 68,027,862  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2020 - October |&nbsp;20.9 GB |&nbsp;&nbsp; 70,572,373  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2020 - November |&nbsp;23.2 GB |&nbsp;&nbsp; 78,268,317  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2020-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2020 - December |&nbsp;26.6 GB |&nbsp;&nbsp; 89,422,803  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2021 - January |&nbsp;30.8 GB |&nbsp;&nbsp; 95,853,038  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2021 - February |&nbsp;28.9 GB |&nbsp;&nbsp; 89,892,001  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2021 - March |&nbsp;32.4 GB |&nbsp; 100,023,791  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2021 - April |&nbsp;32.1 GB |&nbsp;&nbsp; 99,184,138  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2021 - May |&nbsp;32.7 GB |&nbsp; 101,011,629  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2021 - June |&nbsp;29.7 GB |&nbsp;&nbsp; 92,190,803  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2021 - July |&nbsp;29.8 GB |&nbsp;&nbsp; 92,193,352  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2021 - August |&nbsp;30.4 GB |&nbsp;&nbsp; 93,679,328  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2021 - September |&nbsp;28.5 GB |&nbsp;&nbsp; 88,133,339  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2021 - October |&nbsp;28.5 GB |&nbsp;&nbsp; 88,092,721  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2021 - November |&nbsp;28.2 GB |&nbsp;&nbsp; 87,113,345  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2021-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2021 - December |&nbsp;31.1 GB |&nbsp;&nbsp; 95,600,810  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2022 - January |&nbsp;33.2 GB |&nbsp; 102,110,423  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2022 - February |&nbsp;&nbsp;&nbsp;28 GB |&nbsp;&nbsp; 86,339,501  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2022 - March |&nbsp;29.4 GB |&nbsp;&nbsp; 91,140,030  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2022 - April |&nbsp;28.1 GB |&nbsp;&nbsp; 87,200,457  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2022 - May |&nbsp;28.8 GB |&nbsp;&nbsp; 89,300,578  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2022 - June |&nbsp;28.3 GB |&nbsp;&nbsp; 87,649,571  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2022 - July |&nbsp;29.8 GB |&nbsp;&nbsp; 92,055,571  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2022 - August |&nbsp;&nbsp;&nbsp;30 GB |&nbsp;&nbsp; 92,670,440  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2022 - September |&nbsp;28.9 GB |&nbsp;&nbsp; 89,174,810  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2022 - October |&nbsp;&nbsp;&nbsp;30 GB |&nbsp;&nbsp; 92,629,656  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2022 - November |&nbsp;28.9 GB |&nbsp;&nbsp; 89,319,297  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2022-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2022 - December |&nbsp;30.2 GB |&nbsp;&nbsp; 93,501,009  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2023 - January |&nbsp;33.5 GB |&nbsp; 103,178,407  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2023 - February |&nbsp;31.8 GB |&nbsp;&nbsp; 98,471,537  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2023 - March |&nbsp;34.9 GB |&nbsp; 108,201,825  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2023 - April |&nbsp;32.9 GB |&nbsp; 101,706,224  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2023 - May |&nbsp;33.7 GB |&nbsp; 104,193,153  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2023 - June |&nbsp;31.2 GB |&nbsp;&nbsp; 96,641,906  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2023 - July |&nbsp;30.8 GB |&nbsp;&nbsp; 95,300,285  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2023 - August |&nbsp;31.2 GB |&nbsp;&nbsp; 96,118,124  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2023 - September |&nbsp;30.3 GB |&nbsp;&nbsp; 93,218,629  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2023 - October |&nbsp;30.8 GB |&nbsp;&nbsp; 94,922,297  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2023 - November |&nbsp;&nbsp;&nbsp;30 GB |&nbsp;&nbsp; 92,389,636  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2023-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2023 - December |&nbsp;31.7 GB |&nbsp;&nbsp; 96,909,211  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2024 - January |&nbsp;32.4 GB |&nbsp;&nbsp; 98,994,760  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2024 - February |&nbsp;29.8 GB |&nbsp;&nbsp; 91,567,975  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2024 - March |&nbsp;31.1 GB |&nbsp;&nbsp; 95,804,114  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2024 - April |&nbsp;29.6 GB |&nbsp;&nbsp; 91,377,787  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2024 - May |&nbsp;30.7 GB |&nbsp;&nbsp; 94,400,051  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2024 - June |&nbsp;29.1 GB |&nbsp;&nbsp; 89,342,529  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2024 - July |&nbsp;29.3 GB |&nbsp;&nbsp; 90,106,180  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2024 - August |&nbsp;&nbsp;&nbsp;30 GB |&nbsp;&nbsp; 92,198,878  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2024 - September |&nbsp;28.6 GB |&nbsp;&nbsp; 87,713,219  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2024 - October |&nbsp;30.7 GB |&nbsp;&nbsp; 94,254,891  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2024 - November |&nbsp;29.6 GB |&nbsp;&nbsp; 90,847,982  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2024-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2024 - December |&nbsp;31.6 GB |&nbsp;&nbsp; 96,587,411  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2025 - January |&nbsp;32.9 GB |&nbsp; 100,412,379  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2025 - February |&nbsp;29.2 GB |&nbsp;&nbsp; 89,430,612  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-03.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2025 - March |&nbsp;31.8 GB |&nbsp;&nbsp; 97,512,351  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-04.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2025 - April |&nbsp;29.8 GB |&nbsp;&nbsp; 91,757,350  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-05.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2025 - May |&nbsp;30.7 GB |&nbsp;&nbsp; 94,068,115  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-06.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2025 - June |&nbsp;29.7 GB |&nbsp;&nbsp; 91,189,178  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-07.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2025 - July |&nbsp;30.4 GB |&nbsp;&nbsp; 93,092,772  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-08.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;&nbsp;2025 - August |&nbsp;30.2 GB |&nbsp;&nbsp; 92,695,519  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-09.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;2025 - September |&nbsp;28.3 GB |&nbsp;&nbsp; 87,049,890  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-10.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2025 - October |&nbsp;29.9 GB |&nbsp;&nbsp; 91,549,148  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-11.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2025 - November |&nbsp;29.4 GB |&nbsp;&nbsp; 90,633,152  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2025-12.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2025 - December |&nbsp;30.8 GB |&nbsp;&nbsp; 94,847,276  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2026-01.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;&nbsp;2026 - January |&nbsp;30.7 GB |&nbsp;&nbsp; 94,604,722  games</option>'
    BuildPage += '<option value="lichess_db_standard_rated_2026-02.pgn.zst"  style="font-family: \'Courier New\', Courier, monospace;">&nbsp;&nbsp;2026 - February |&nbsp;27.8 GB |&nbsp;&nbsp; 84,600,043  games</option>'
    BuildPage += '</select>'
    BuildPage += '<br><button type="submit" style="font-size: 24px; background-color: black; color: gold; border: 2px solid gold; padding: 15px 30px; cursor: pointer; border-radius: 8px; font-weight: bold; margin: 20px auto; display: block;">Submit</button>'
    BuildPage += '</form>'

    if fileNameSelected:
        BuildPage += '<h3>Data File selected is: ' + fileNameSelected + '</h3>'

    BuildPage += "<br><br>" + AppLog     
    BuildPage += "</div>"    
    
    return BuildPage



if __name__ == '__main__':
    app.run(debug=True)
