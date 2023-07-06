import random
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image, ImageDraw
import copy
import os

# load the data representing the initial position of robots, victims and hospitals
lines = open('config.txt').read().splitlines()
data = [line.split() for line in lines]
WIDTH = len(data[0])
HEIGHT = len(data)

# load the ground
lines = open('terrain.txt').read().splitlines()
ground = [line.split() for line in lines]

master = Tk()

#Define some constant
ORIENTATIONS = ['N','E','S','W']
OFFSETS = [[-1,0],[0,1],[1,0],[0,-1]]
ROTATIONS = [0,-90,180,90]

ACTION_PRIORITIES={
2 : ['take','drop'],
1 : ['move','left','right'],
0 : 'uturn'
}

#Define some global parameters
BASE_IMAGES = {}
GROUND_IMAGES = {
    '1' : 'droiteHorizontale',
    '2' : 'droiteVerticale',
    '3' : 'intersectionN',
    '4' : 'intersectionE',
    '5' : 'intersectionS',
    '6' : 'intersectionO',
    '7' : 'virageNE',
    '8' : 'virageNO',
    '9' : 'virageSE',
    '10' : 'virageSO'
}

#Possible moves from a position according to the ground
CAN_MOVE = {
    '1' : ['E','W'],
    '2' : ['N','S'],
    '3' :  ['N','E','W'],
    '4' : ['N','E','S'],
    '5' : ['S','E','W'],
    '6' : ['N','S','W'],
    '7' : ['NE','SW'],
    '8' : ['NW','SE'],
    '9' : ['SE','NW'],
    '10' : ['SW','NE']
}

#Load images
for file in next(os.walk('img'))[2]:
    name = file[:-4]
    img = Image.open("img\{}.png".format(name)).convert('RGBA')
    BASE_IMAGES[name] = img

#Load ground images
for name in GROUND_IMAGES.keys():
    filename = GROUND_IMAGES[name]
    img = Image.open("img/terrain/{}.png".format(filename)).convert('RGBA')
    BASE_IMAGES[name] = img

def load_image(element,ground_element):
    """
    :param element: name of the element
    :param ground_element: name of the ground element
    :return: Image containing the ground + the element
    """
    ground = BASE_IMAGES[ground_element]
    ground = copy.deepcopy(ground)
    ground = ground.resize((100, 100))

    name = element[0]
    if name in BASE_IMAGES:
        img = BASE_IMAGES[name]
        img = copy.deepcopy(img)
        if name == 'R':
            img = img.rotate(ROTATIONS[ORIENTATIONS.index(element[-1])])
        if name in ['R','A','C']:
            n = element[1]
            I1 = ImageDraw.Draw(img)
            I1.text((5, 5), n, fill=(0, 0, 0))
        img = img.resize((40,40))
        ground.paste(img, (30, 30),mask=img)
    return ImageTk.PhotoImage(ground)

def checkInWidthRange(value):
    return  0 <= value and value < WIDTH

def checkInHeightRange(value):
    return  0 <= value and value < HEIGHT

class Robot():

    def __init__(self,simulator,name,orientation,position=[0,0],max_stock=2):
        """
        :param simulator: simulator (for communication)
        :param name: name of the robot
        :param orientation: initial orientation of the robot
        :param position: initial position of the robot
        :param max_stock: the number of victims that can be carried
        """
        self.name = name
        self.max_stock = max_stock
        self.position = position
        self.stock = []
        self.simulator = simulator
        self.orientation = orientation



    def turn(self,orientation):
        self.orientation = orientation
        self.simulator.update_orientation(self)

    def turnRight(self):
        self.turn(self.simulator.compute_newOrientation(self.orientation,1))
        self.move()

    def turnLeft(self):
        self.turn(self.simulator.compute_newOrientation(self.orientation,-1))
        self.move()

    def drop(self):
        """
        Drop all the victims
        :return:
        """
        self.stock = []

    def update_position(self,new_position):
        self.position = new_position

    def take(self):
        """
        Take a victim
        :return:
        """
        element = simulator.takeVictime(self.position)
        self.stock.append(element)

    def move(self):
        """
        Move to a new position (1 step in the current orientation)
        :return:
        """
        x, y = self.position
        i , j = OFFSETS[ORIENTATIONS.index(self.orientation)]
        new_position = [x + i, y + j]
        new_orientation = simulator.moveElement(self.position, self.orientation)
        self.update_position(new_position)
        self.turn(new_orientation)

    def uturn(self):
        self.turn(self.simulator.compute_newOrientation(self.orientation,-2))


    def left(self):
        self.turnLeft()

    def right(self):
        self.turnRight()

    def nop(self):
        pass

    def doAction(self):
        actions_list = ['drop','take','move','left','right','uturn']
        if len(self.stock) == 0:
            actions_list.remove('drop')
        else:
            action = self.simulator.check_action(self, 'drop', self.orientation)
            if action == 'drop':
                self.drop()
                return
        if len(self.stock)==self.max_stock:
            actions_list.remove('take')
        else:
            action = self.simulator.check_action(self, 'take', self.orientation)
            if action == 'take':
                self.take()
                return

        while len(actions_list)>0:
            action_index = random.randint(0,len(actions_list)-1)
            action = actions_list[action_index]
            print(self.name,'is asking for',action,end=' ')
            orientation = self.orientation
            if action == 'left':
                orientation = self.simulator.compute_newOrientation(orientation,-1)
            elif action == 'right':
                orientation = self.simulator.compute_newOrientation(orientation,1)
            action_name = self.simulator.check_action(self,action,orientation)
            print(' ===> got : ',action_name,'stock',self.stock)

            if action_name=='nop':
                actions_list.remove(action)
            else:
                f = getattr(self, action_name)
                f()
                break

class Simulator():
    def __init__(self,data):
        """
        :param data: inital position of each element
        """
        self.data = data
        self.robots = []
        self.images = self.load_images()
        self.labels = self.draw_images()
        self.victim_count = 0
        self.saved_count = 0
        self.init_world()

    def init_world(self):
        """
        Creats robots from the initial positions, count victims
        :return:
        """
        for i, line in enumerate(self.data):
            for j, element in enumerate(line):
                    if 'R' in element:
                        self.robots.append(Robot(self,element[:-1],element[-1],[i,j]))
                    if 'P' in element:
                        self.victim_count+=1

    def compute_newOrientation(self,orientation,direction):
        """
        Computes the new orientation from the current one and a direction (right or left)
        :param orientation: current direction
        :param direction:
        :return:
        """
        currant_orientation_index = ORIENTATIONS.index(orientation)
        new_orientation_index = (currant_orientation_index + direction) % len(ORIENTATIONS)
        return ORIENTATIONS[new_orientation_index]

    def update_orientation(self,robot):
        """
        Updates the orientation of a robot
        :param robot:
        :return:
        """
        element = self.getDataElement(robot.position)
        new_element = element[:-1]+robot.orientation
        self.setDataElement(robot.position,new_element)

    def getDataElement(self,position):
        x,y = position
        return self.data[x][y]

    def takeVictime(self,position):
        """
        Removes a victim from the world
        :param position:
        :return:
        """
        victime = self.getDataElement(position)
        new_elment = 'R'+victime[1:]
        self.setDataElement(position,new_elment)
        return victime


    def setDataElement(self,position,element):
        x,y = position
        self.data[x][y]=element

    def update(self):
        """
        Updates the GUI
        :return:
        """
        self.images = self.load_images()
        self.update_images()

    def load_images(self):
        images = []
        for i,line in enumerate(self.data):
            in_a_line = []
            for j,element in enumerate(line):
                in_a_line.append(load_image(element,ground[i][j]))
            images.append(in_a_line)
        return images

    def getNewPositionFromOrientation(self,position,orientation):
        """
        Computes new position according to the current one, and the current orientation
        :param position: current position
        :param orientation: current orientation
        :return:
        """
        x,y = position
        i,j = 0,0
        if orientation == 'N':
            i = -1
        elif orientation == 'S':
            i = 1
        elif orientation == 'E':
            j = 1
        elif orientation == 'W':
            j = -1
        return [x+i,y+j]

    def canMove(self,robot,orientation):
        """
        Checks if the robot can move according the specified orientation
        :param robot:
        :param orientation:
        :return:
        """
        x, y = robot.position
        i, j = self.getNewPositionFromOrientation(robot.position,orientation)
        available_direction = [x[0] for x in CAN_MOVE[ground[x][y]]]
        return checkInHeightRange(i) and checkInHeightRange(j) and not self.data[i][j][0] in ['X', 'A', 'C', 'R'] and orientation in available_direction

    def moveElement(self,position,orientation):
        """
        Moves an element in the world
        :param position:
        :param orientation:
        :return:
        """
        x, y = position
        i, j = self.getNewPositionFromOrientation(position, orientation)
        if 'C' in self.data[x][y]:
            new_element = 'H'
        elif 'A' in self.data[x][y]:
            new_element = 'P'
        else:
            new_element = '_'

        if self.data[i][j] == '_':
            self.data[i][j] = 'R'+self.data[x][y][1:]
            self.data[x][y] = new_element
        elif self.data[i][j] == 'H':
            self.data[i][j] = 'C'+self.data[x][y][1:]
            self.data[x][y] = new_element
        elif self.data[i][j] == 'P':
            self.data[i][j] = 'A'+self.data[x][y][1:]
            self.data[x][y] = new_element

        available_direction = [D for D in CAN_MOVE[ground[x][y]] if D[0]==orientation]
        new_direction = available_direction[0][-1]
        return new_direction

    def check_action(self,robot,action,orientation):
        """
        Checks if the action send by the robot is correct
        :param robot:
        :param action:
        :param orientation:
        :return: the same action if correct, otherwise 'nop'
        """
        if action == 'uturn':
            response = 'uturn'
        elif action == 'take' and self.canTake(robot.position):
            response = 'take'
        elif action == 'drop' and self.canDrop(robot.position):
            response = 'drop'
            self.saved_count +=len(robot.stock)
        elif action in ['move','left','right'] and self.canMove(robot,orientation):
            response = action
        else:
            response = 'nop'
        return response


    def draw_images(self):
        labels = []
        for i, line in enumerate(self.images):
            label_line = []
            for j, element in enumerate(line):
                label = Label(master, image=element)
                label.grid(row=i, column=j)
                label_line.append(label)
            labels.append(label_line)
        return labels

    def update_images(self):
        for i, line in enumerate(self.images):
            for j, element in enumerate(line):
                self.labels[i][j].configure(image=element)
                self.labels[i][j].image = element

    def move(self):
        for robot in self.robots:
            robot.doAction()

    def canTake(self,position):
        return self.getDataElement(position)[0] == 'A'

    def canDrop(self,position):
        return self.getDataElement(position)[0] == 'C'

simulator = Simulator(data)

for x in simulator.robots:
    print(x.name,x.position)
text = Label(master,text="Informations")
text.grid(row=0, column=5)
text = Label(master,text="Nombre de victimes à sauver :")
text.grid(row=1, column=5)
victims_count = Label(master,text=str(simulator.victim_count))
victims_count.grid(row=2, column=5)
text = Label(master,text="Nombre de victimes sauvées :")
text.grid(row=3, column=5)
saved_count = Label(master,text="")
saved_count.grid(row=4, column=5)
master.update()
master.after(500)

#While there is a victim to save
while simulator.saved_count<simulator.victim_count:
    #Do actions
    simulator.move()
    #Update the world
    simulator.update()

    #update saved count
    saved_count.configure(text=str(simulator.saved_count))
    #Update the GUI
    master.update()
    #sleep 200ms
    master.after(200)

master.mainloop()