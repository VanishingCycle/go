from turtle import update
from go_player import GlobalPlayer
from move_handler import MoveHandler
from go_board import GoBoard

#Create a player, and create the corresponding local player.

Nicolas = GlobalPlayer("Nicolas",30) 
Honglu = GlobalPlayer("Honglu",30)

#Create the corresponding local player, color : black

nicolas = Nicolas.get_local("black")
honglu = Honglu.get_local("white")

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
honglu.move = (4,5)
print(m.check_capture(honglu)) 

#check_suicide : 

m.goban[4][5] = "white"
nicolas.move = (4,4)
print (m.check_suicide(nicolas))

#check definition of GoBoard
blank_goban = [["void" for x in range(19)] for y in range(19)]
m.goban = blank_goban
m.groups = []
print("checking GoBoard...")
MyBoard = GoBoard(black_player = Nicolas, white_player = Honglu, black = nicolas, white = honglu, move_handler=m)
print(MyBoard.move_handler.groups)
honglu.move = (1,1)
MyBoard.update_groups(honglu)
print(MyBoard.move_handler.groups)
honglu.move = (1,2)
MyBoard.update_groups(honglu)
print(MyBoard.move_handler.groups)
nicolas.move = (5,4)
MyBoard.update_move(nicolas)
print(MyBoard.move_handler.groups)
nicolas.move = (4,4)
MyBoard.update_move(nicolas)
print(MyBoard.move_handler.groups)
honglu.move = (12,12)
MyBoard.update_move(honglu)
print(MyBoard.move_handler.groups)

#check the play function 

blank_goban = [["void" for x in range(19)] for y in range(19)]
m.goban = blank_goban
m.groups = []

