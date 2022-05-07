goban = [[0 for x in range(19)] for y in range(19)]
groups = []  #list of all the groups of stones
black_prisoners = 0
white_prisoners = 0

def play_go():
    i=0
    while i > -1 :
        if i%2 == 0 :
            n=int(input("first coordinate:"))
            m=int(input("second coordinate:"))
            if goban[n][m] !=0 :
                i = i -1
                print("Move not valid.")
            else :
                play_black(n,m)
                print_goban()
        else :
            n = int(input("first coordinate:"))
            m = int(input("second coordinate:"))
            if goban[n][m] != 0:
                i = i - 1
                print("Move not valid.")
            else:
                play_white(n,m)
                print_goban()
        i +=1


def print_goban():
    for x in range(19):
        print(goban[x])

def play_black(a,b):
    if a in range(19) and b in range(19):
        check_capture(2,a,b)
        goban[a][b] = 1
        update_group(1,a,b)
    else:
        print("Coordinate not valid.")

def play_white(a,b):
    if a in range(19) and b in range(19):
        check_capture(1,a,b)
        goban[a][b] = 2
        update_group(2,a,b)
    else:
        print("Coordinate not valid.")

#return all surrounding cases of a given case
def surrounding_cases(a,b):
    sur = []
    if a -1 in range(19):
        sur.append([a-1,b])
    if a + 1 in range(19):
        sur.append([a+1,b])
    if b - 1 in range(19):
        sur.append([a,b-1])
    if b + 1 in range(19):
        sur.append([a,b+1])
    return sur

# return the group containing the stone (a,b)
def group_belonging(a,b):
    if goban[a][b] != 0:
        for x in groups:
            if [a,b] in x:
                return x

# upload list of groups when a stone of type n is played in (a,b)
def update_group(n,a,b):
    sur = surrounding_cases(a,b)
    sur_same_color = []
    for x in sur:
        if n== goban[x[0]][x[1]]:
            sur_same_color.append(x)
    if not sur_same_color:
        groups.append([[a,b]])
    else:
        oldgroups = []
        for x in sur_same_color:
            for y in groups:
                if x in y:
                    oldgroups.append(y)
                    groups.remove(y)
        newgroup = []
        for y in oldgroups:
            newgroup = newgroup + y
        newgroup.append([a,b])
        groups.append(newgroup)
    return groups

def boundary_group(g):
    boundary = []
    big_boundary = []
    for x in g:
        big_boundary = big_boundary + surrounding_cases(x[0],x[1])
    for y in big_boundary:
        if y not in g and y not in boundary:
            boundary.append(y)
    return boundary


# A stone of type 3-n has been played, we want to know if group of type n have been captured
def check_capture(n,a,b):
    global black_prisoners
    global white_prisoners
    for y in surrounding_cases(a,b):
        for x in groups:
            if y in x and goban[y[0]][y[1]] == n:
                u=boundary_group(x)
                d=0
                for v in u:
                    if v != [a, b]:
                        if goban[v[0]][v[1]] == 0 or goban[v[0]][v[1]] == n :
                            d = 1
                if d == 0 :
                    if n == 1 :
                        black_prisoners += len(x)
                    if n == 2 :
                        white_prisoners += len(x)
                    for y in x:
                        goban[y[0]][y[1]] = 0
                    groups.remove(x)


play_go()