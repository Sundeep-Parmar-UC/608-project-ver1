Data 608  - G5-Rita Group Project Code Repository

Michael Morgan, 30301873, michael.morgan@ucalgary.ca  
Sundeep Parmar, 30301836, sundeep.parmar@ucalgary.ca  
Yu Ling Wong, 30297454, yuling.wong@ucalgary.ca

Chess Bot: Playing Chess Through Human Game Patterns

This repository contains three applications:    
ingest.py  
chessbot.py  
ingest.ipynb  
DB-Prepare.ipynb

All four files begin with the code chunk to connect to the RDS server (MySQL).
Define the ConnectionString variable with the connection details provided by RDS.


The snark.py file requires an API key. This key is generated on Google AI Studio.   
https://aistudio.google.com/api-keys  

There are two folders:  
static/ChessBoard/*    - this is used by chessbot.py to draw the game board
Documentation/*   - contains various documents created to guide the project
