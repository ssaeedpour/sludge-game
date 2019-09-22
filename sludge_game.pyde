#TUBE DATA

#tubes_info: {tube id: x,y on pic} holds the info of the tubes
#downleft, flow down,entrance flow, exit flow, x inc, y inc (to find next pos), size of tube,  time for animation, count for animation,max time
tubes_info = {"dl":[[700,0,"d","l",80],[700,100,"r","u",80]], #DOWN LEFT: DLD 1ST, DLU 2ND
              "dr":[[700,200,"d","r",80],[700,300,"l","u",80]], #DOWN RIGHT: DRD 1ST, DRU 2ND
               "ul":[[700,400,"r","d",80],[700,500,"u","l",80]], #UP LEFT: ULD 1ST, ULU 2ND
               "ur":[[700,600,"l","d",80],[700,700,"u","r",80]], #UP RIGHT: URD 1ST, URU 2ND
               "ud":[[700,800,"d","d",70],[700,900,"u","u",70]], #UP DOWN: UDD 1st, UDU 2nd
               "lr":[[700,1000,"l","l",70],[700,1100,"r","r",70]]} #LEFT RIGHT: LRL 1ST, LRR 2ND         

indi_data = [[[0,0,True, 50] for n in range (6)] for n in range (6)] #time,increment, whether the tube can be moved or not, variable for modulo
#FLOW VARIABLES 
dict_of_dir = {"d":[1,0],"u":[-1,0],"l":[0,-1],"r":[0,1]} #WHERE IN THE ARRAY TO LOOK BASED ON THE DIRECTION OF FLOW



l_of_keys = ["dl","dr","ul","ur","ud","lr"]
x = 0
y = 0


#BOX DATA
curr_position = [0,0,400,100] #curr position in index, curr position on screen (used for the rectangle)
switch_pos = [] #holds the index and coordinates of the two tubes that'll switch 


def setup():
    global info,sprite,tube_class,curr_flow,tubes_info,tube_grid,dict_of_dir,grid_class,curr_flow,indi_data,up,left,down,right
    size (1000,600)
    sprite = loadImage("last3.png")
    left = loadImage("left.png")
    right = loadImage("right.png")
    up = loadImage("up.png")
    down = loadImage("down.png")
    info = loadImage ("info2.png")
    
    
    
    grid_class = Grid()
    tube_class = Tubes()
    
    for n in range (6):
        for i in range (6):
            grid_class.make_grid(n,i) #make the grid with tube names
            
            
    #initialize the enter/exit coordinates
    enter = grid_class.enter_init()
    exit_ = grid_class.exit_init()

    
    
def draw():
    global sprite,tube_class,x,y,l_of_keys,tube_grid,curr_position,switch_pos,info
    background (0)
    grid_class.switch()
    fill (0)
    stroke(78,178,72)
    rect(curr_position[2],curr_position[3],71,71) #current position rectangle
    image (info,70,150,250,250)
    tube_class.flow (grid_class.curr_flow[1],grid_class.curr_flow[2],grid_class.curr_flow[3],grid_class.curr_flow[0])
    
    for n in range (6):
        y = 100 + (75 * n)
        for i in range (6):
            x = 400 + (75 * i)
            tube_class.draw_tube(x,y,n,i)#x,y location in processing, n, i location in tubes_type list  
    # curr_flow = [0,grid_class.enter[0], grid_class.enter[1],0] #direction of flow, row in array, column in array
    #print grid_class.leave
    #drawing the entrance/exit arrows
    if grid_class.enter[0] == 5: #start is on bottom row
            image (up, 400 + grid_class.enter[1]*75, 540,70,70)
    elif grid_class.enter[0] == 0: #start is at top row
            image(down,400 + grid_class.enter[1]*75 , 30,70,70)
    else:
            if grid_class.enter[1] == 5: #start from right
                 image(left,830, 100+ grid_class.enter[0] *75,70,70)
            elif grid_class.enter[1] == 0: #start from left
                image(right,330, 100 + grid_class.enter[0] * 75,70,70)

    if grid_class.leave[0] == 5: #start is on bottom row
            image (down, 400 + grid_class.enter[1]*75, 540,70,70)
    elif grid_class.leave[0] == 0: #start is at top row
            image(up,400 + grid_class.enter[1]*75 , 30,70,70)
    else:
            if grid_class.leave[1] == 5: #start from right
                image(right,830, 100+ grid_class.enter[0] *75,70,70)
            elif grid_class.leave[1] == 0: #start from left
                image(left,330, 100 + grid_class.enter[0] * 75,70,70)
    
    
class Grid:
    global  tubes_info,l_of_keys,switch_pos,up,left,down,right
    def __init__(self):
        self.tube_grid = [[0 for n in range (6)] for n in range (6)] #makes the grid where tubes will be stored & DRAWN BASED ON THIS LIST
        self.rand_index = [[int(random(0,6)) for n in range (6)] for n in range (6)] #makes random integers
        #code below used to determine start/end position
        self.enter = [int(random(0,6)),0] #y,x
        self.elpos_l = [0,6] 
        
    def exit_init(self): 
            self.leave = [int(random(0,6)),0]
            if self.leave[0] == 5 or self.leave[0] == 0:
                self.leave[1] = int(random (0,6))
            else:
                self.leave[1] = self.elpos_l[int(random(0,1))]
            if self.leave[0] == self.enter[0] and self.leave[1] == self.enter[1]:
                #self.leave = [int(random(0,6)),0]
                self.exit_init()
            print "start:" , self.enter, "exit:", self.leave, "self.curr_flow", self.curr_flow
        
            
    def enter_init(self):
        #code below determines the start position & places a compatible tube at that position
        if self.enter[0] == 5: #start is on bottom row
            self.enter[1] = int(random (0,6))
            self.curr_flow = ["u",self.enter[0],self.enter[1],1]
            self.tube_grid [self.enter[0]][self.enter[1]] = "ud"
            
        elif self.enter[0] == 0: #start is at top row
            self.enter[1] = int(random (0,6))
            self.curr_flow = ["d",self.enter[0],self.enter[1],0]
            self.tube_grid [self.enter[0]][self.enter[1]] = "ud"

        else:
            self.enter[1] = self.elpos_l[int(random(0,1))]
            if self.enter[1] == 5: #start from right
                self.curr_flow = ["l",self.enter[0],self.enter[1],0]
                self.tube_grid [self.enter[0]][self.enter[1]] = "lr"
                
            elif self.enter[1] == 0: #start from left
                self.curr_flow = ["r",self.enter[0],self.enter[1],1]
                self.tube_grid [self.enter[0]][self.enter[1]] = "lr"

       
        
    def make_grid(self,n,i): #Makes the list of tube
        #inputs a random tube key into the grid 
        self.tube_grid[n][i] = l_of_keys[self.rand_index[n][i]] #tube_grid is the grid. l_of_keys is a way to input the type of tube into the list
        
    def switch(self):
        #gonna need tube_class.tube_grid and tube_class.x and tube_class.y
        if len(switch_pos) == 1:
                rect (switch_pos[0][2],switch_pos[0][3],71,71)
        elif len(switch_pos) == 2: 
                rect(switch_pos[1][2],switch_pos[1][3],71,71)
        if len(switch_pos) >= 2:
            self.tube_grid [switch_pos[0][1]] [switch_pos[0][0]],self.tube_grid [switch_pos[1][1]] [switch_pos[1][0]] = self.tube_grid [switch_pos[1][1]] [switch_pos[1][0]], self.tube_grid [switch_pos[0][1]] [switch_pos[0][0]]
            switch_pos[:] = []         
        
        
class Tubes:
    global tubes_info,l_of_keys,dict_of_dir, grid_class,curr_flow,indi_data
    def __init__(self):
        self.inc = [0]
        self.directions = ["r","l","d","u"]
        self.count = 0
        self.time = 0
    def draw_tube(self,x,y,n,i): #x,y location in processing, n, i location in tubes_type list   
        self.x = x
        self.y = y
        #tubes_cord[key][0] where key is self.tube_grid[n][i] 
        #indi_data = [[[70,0,0] for n in range (6)] for n in range (6)] size, count, time
        copy (sprite,tubes_info[grid_class.tube_grid[n][i]][grid_class.curr_flow[3]][0] - (indi_data[n][i][0]* 100), tubes_info[grid_class.tube_grid[n][i]][grid_class.curr_flow[3]][1] ,100,100,self.x,self.y,70,70)
        #(x,y(on pic), width,height (on pic),x,y(on screen)width, height (on screen))"""
    def flow(self,y,x,index, flow): #initial x y & flow is from current flow, index (index of the direction tube), direction of current flow
        #code below plays the animation once
        indi_data[y][x][1] += 1 #time += 1
        fill (27,184,43)
        
        if  indi_data[y][x][1]>= tubes_info[ grid_class.tube_grid[y][x]] [index] [4]: #if time >= time_limit
            indi_data[y][x][0] =  (tubes_info[ grid_class.tube_grid[y][x]] [index] [4]) / 10 - 1 #results in the last sprite. Tube stays in "full state" 
            if (y != grid_class.leave[0] and  x != grid_class.leave[1]) and (y + dict_of_dir[flow][0] <0  or x + dict_of_dir[flow][1] <0 or y + dict_of_dir[flow][0] >5  or x + dict_of_dir[flow][1] >5):
                fill (22,139,34)
                text("You Win!", 165,360)
                print "uahhhh" 
            elif y == grid_class.leave[0] and x == grid_class.leave[1]:
                fill (22,139,34)
                text ("You Win!", 165, 360)
                
            elif flow == tubes_info[grid_class.tube_grid [y + dict_of_dir[flow][0]] [x + dict_of_dir[flow][1]]]  [0] [2]:
                #print 0, "current:",flow,"next",tubes_info[grid_class.tube_grid [y + dict_of_dir[flow][0]] [x + dict_of_dir[flow][1]]]  [0] [3]
                self.flow(y + dict_of_dir[flow][0] ,x + dict_of_dir[flow][1],0, tubes_info[grid_class.tube_grid [y + dict_of_dir[flow][0]] [x + dict_of_dir[flow][1]]]  [0] [3])
                
            elif flow == tubes_info[grid_class.tube_grid [y + dict_of_dir[flow][0]] [x + dict_of_dir[flow][1]]]  [1] [2]:
                #print 1, "current:",flow,"next",tubes_info[grid_class.tube_grid [y + dict_of_dir[flow][0]] [x + dict_of_dir[flow][1]]]  [1] [3]
                self.flow(y + dict_of_dir[flow][0],x + dict_of_dir[flow][1],1, tubes_info[grid_class.tube_grid [y + dict_of_dir[flow][0]] [x + dict_of_dir[flow][1]]]  [1] [3])
            else:
                fill (22,139,34)
                text("You Win!", 165,360)
                print "heehee"
        elif indi_data[y][x][0] > 0:
             indi_data[y][x][2] = False
        elif indi_data[y][x][1] % indi_data[y][x][3] == 0: #if time %10 = 0 (used modulo to slow down the animation)
            indi_data[y][x][0] += 1 #count += 1
        else:
            text("In Progress", 160,360)

def keyPressed():        
    global curr_position,switch_pos,space_pos,indi_data,l_of_keys
    if keyCode == LEFT:
        if curr_position[0] >0:
            curr_position [0] -= 1
            curr_position[2] -= 75
        else:
            curr_position[0] = curr_position[0]
    if keyCode == RIGHT:
        if curr_position[0] <= 4:
            curr_position [0] += 1
            curr_position[2] += 75
        else:
            curr_position[0] = curr_position[0]
    if keyCode == UP:
        if curr_position[1] > 0:
            curr_position [1] -= 1
            curr_position[3] -= 75
        else:
            curr_position[1] = curr_position[1]
    if keyCode == DOWN:
        if curr_position[1] <= 4:
            curr_position [1] += 1
            curr_position[3] += 75
        else:
            curr_position[1] = curr_position[1]
    if key == " " and indi_data[curr_position[1]] [curr_position[0]] [2] == True:
        switch_pos.append(curr_position[:])

    if keyCode == ENTER:
        for n in range (6):
            for i in range (6):
                for x in range (3):
                    indi_data[n][i][x] = 1
        for n in l_of_keys:
            tubes_info[n][0][3] /= 10
            tubes_info[n][1][3] /= 10
            
    

    
    
    
    
    
    
    
    
    
    
    
