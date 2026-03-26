# receive File name from lichess database
# receive month value
# receive year value

# check if file has been loaded,   return -1 if loaded

# if not, then create stub and return file_id

from datetime import datetime


def files(Filename,Month_value,Year_value,SQLconnect):

    sqlstatement = "SELECT id,NumGamesTotal FROM files WHERE  filename = '" + Filename + "'"
    SQLconnect.execute(sqlstatement)
    records = SQLconnect.fetchall()
    NumofFiles = len(records)  
    if(NumofFiles == 0):   # no entry
        now = datetime.now()
        insert_query = "INSERT INTO files (filename, Month_value,Year_value,DateTimeLoaded) VALUES (%s, %s, %s, %s)"
        SQLconnect.execute(insert_query, (Filename, Month_value,Year_value,now))
        InsertedRecord = SQLconnect.lastrowid
        print(f"File Record inserted. ID: {InsertedRecord}")
        return InsertedRecord    
    else:
        print(f"Files Found: {NumofFiles}")
        for row in records:
            if row[1]:
                return -1
            else:
                print("File loaded did not complete so continuing") 
                return row[0]
        
        return -1
    return -1


def files_update(file_id,Ingested,TotalGames,FileSize,SQLconnect):
    
    now = datetime.now()
    update_query = "UPDATE files SET DateTimeLoaded = %s,NumGamesTotal = %s, NumGamesIngested = %s, File_size = %s  WHERE id = %s"
    SQLconnect.execute(update_query, (now, TotalGames,Ingested,FileSize,file_id))
    print("Record updated.")