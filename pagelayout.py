# receive N/a

# return html table to draw BaseBoard
# return html table to draw BaseMovesList

def pagelayout():
    BaseBoard = [[['<td><img src="',r'/ChessBoard/Black.jpg','" width="56" alt="Chess Board"></td>'] for _ in range(8)] for _ in range(8)]


    BaseMovesList = [['<td style="padding: 6px; border: 2px solid #ddd; font-weight: bold;">','1','</td><td style="padding: 6px; border: 2px solid #ddd;">','e4','</td><td style="padding: 6px; border: 2px solid #ddd;">','e5','</td>'] for _ in range(1)]

    return BaseBoard,BaseMovesList
    