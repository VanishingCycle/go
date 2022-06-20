from turtle import update
from go_player import GlobalPlayer
from go_player import Move 
from move_handler import MoveHandler
from go_board import GoBoard

#Create a player, and create the corresponding local player.

Nicolas = GlobalPlayer("Nicolas",30) 
Honglu = GlobalPlayer("Honglu",30)

#Test of all the methods from MoveHandler : 

m = MoveHandler(rule = "japanese") 

#test opposite function 
print("testing opposite function :")
print(m.opposite("black"))
print(m.opposite("white"))
print(m.opposite("test"))

#test boundary_point
print("computing boundary points of (1,1) and (0,0) :")
u = m.boundary_point((1,1))
v = m.boundary_point((0,0))
print(u)
print(v)

#test boundary_group
print("computing boundary of the group [(1,1),(1,2),(2,2)] :")
MyGroup = [(1,1),(1,2),(2,2)]
print(m.boundary_group(MyGroup))

#check ko (later)


# check_capture : we capture a white stone 
m.goban[3][4] = "white"
m.goban[4][3] = "white"
m.goban[5][4] = "white"
m.goban[4][4] = "black"
m.groups.append([(4,4)])
move1 = Move(position =(4,5), color = "white")
print(m.check_capture(move1)) 

#check_suicide : 

m.goban[4][5] = "white"
move2 = Move( position =(4,4), color = "black")
print (m.check_suicide(move2))

#check definition of GoBoard
print("test for the go board")
blank_goban = [["void" for x in range(19)] for y in range(19)]
m.goban = blank_goban
m.groups = []
print("checking GoBoard...")
MyBoard = GoBoard(black = Nicolas, white = Honglu, move_handler=m)
print(MyBoard.move_handler.groups)
move3 = Move(position =(1,1), color = "white") 
MyBoard.update_move(move3)
print(MyBoard.move_handler.groups)
move4 = Move(position =(1,2), color = "white")
MyBoard.update_move(move4)
print(MyBoard.move_handler.groups)
move5 = Move(position =(5,4), color = "black")
MyBoard.update_move(move5)
print(MyBoard.move_handler.groups)
move6 = Move(position =(4,4), color = "black")
MyBoard.update_move(move6)
print(MyBoard.move_handler.groups)
move7 = Move(position =(12,12), color = "white")
MyBoard.update_move(move7)
print(MyBoard.move_handler.groups)

#check the play function 

blank_goban2 = [["void" for x in range(4)] for x in range(4)]
MyBoard.move_handler.goban = blank_goban2
MyBoard.move_handler.size = (4,4)
MyBoard.move_handler.groups = []
move8 = Move(position =(0,1), color = "white")
MyBoard.update_move(move8)
move9 = Move(position =(1,0), color = "white")
MyBoard.update_move(move9)
move10 = Move(position =(1,1), color = "white")
MyBoard.update_move(move10)
move11 = Move(position =(2,0), color = "black")
MyBoard.update_move(move11)
move12 = Move(position =(2,1), color = "black")
MyBoard.update_move(move12)
move13 = Move(position =(2,2), color = "black")
MyBoard.update_move(move13)
move14 = Move(position =(1,2), color = "black")
MyBoard.update_move(move14)
move15 = Move(position =(0,2), color = "black")
MyBoard.update_move(move15)
print("groups : ", MyBoard.move_handler.groups)
print(MyBoard.count_points())