from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *
import re

class Window(Frame):
    def __init__(self, master=None):

        ####################
        ##### WINDOW #######
        ####################
        Frame.__init__(self, master)

        global file_name # will allow to save a file
        file_name = False

        self.master = master

        self.master.title("Create or modify a configuration file")

        ## MENU CREATION ##
        menu = Menu(master)
        master.config(menu=menu)
        self.file_menu = Menu(menu)
        menu.add_cascade(label="File", menu = self.file_menu)
        self.file_menu.add_command(label="New", command = self.new)
        self.file_menu.add_command(label="Open", command = self.open_file_function)
        self.file_menu.add_command(label="Save", command = self.save)
        self.file_menu.add_command(label="Save As", command = self.save_as)

        ## HELP CREATION ##
        help_button = Menu(master)
        help_button.add_command(label="About", command = self.aide)
        menu.add_cascade(label="Help", menu=help_button)

        ## TEXT EDITING SPACE ##
        # TO MODIFY THE NUMBER OF PLAYERS
        self.players_label = Label(master, text="Nb players", fg="black")
        self.players_label.place(x=10,y=10)
        self.text_players = Text(master, height=1, width=10)
        self.text_players.place(x=100,y=10)

        # TO MODIFY THE NUMBER OF ROBOTS
        self.robots_label = Label(master, text="Nb robots", fg="black")
        self.robots_label.place(x=10,y=40)
        self.text_robots = Text(master, height=1, width=10)
        self.text_robots.place(x=100,y=40)

        # TO MODIFY THE DIMENSION OF THE GRID
        self.dimension_label = Label(master, text="Dimension :", fg="black")
        self.dimension_label.place(x=10,y=70)
        self.rows_label = Label(master, text="Rows", fg="black")
        self.rows_label.place(x=100,y=70)
        self.text_rows = Text(master, height=1, width=5)
        self.text_rows.place(x=150,y=70)
        self.col_label = Label(master, text="Columns", fg="black")
        self.col_label.place(x=220,y=70)
        self.text_col = Text(master, height=1, width=5)
        self.text_col.place(x=290,y=70)

        """
        # TO AFFECT ROBOTS TO PLAYERS
        self.affect_label = Label(master, text="Affectation", fg="black")
        self.affect_label.place(x=10,y=100)
        self.text_affect = Text(master, height=1, width=30)
        self.text_affect.place(x=100,y=100)
        """

        # TO ENTER THE TERRAIN REPRESENTATION
        self.ground_label = Label(master, text="Ground", fg="black")
        self.ground_label.place(x=10,y=130)
        self.text_ground = Text(master, height=8, width=30)
        self.text_ground.place(x=100,y=130)

        ## HELP TO CREATE THE REPRESENTATION OF THE GROUND ##
        # LOAD ALL THE IMAGES #
        self.droiteH_btn = PhotoImage(file="images/droiteHorizontale.png")
        self.droiteV_btn = PhotoImage(file="images/droiteVerticale.png")
        self.virageNE_btn = PhotoImage(file="images/virageNE.png")
        self.virageNO_btn = PhotoImage(file="images/virageNO.png")
        self.virageSE_btn = PhotoImage(file="images/virageSE.png")
        self.virageSO_btn = PhotoImage(file="images/virageSO.png")
        self.intersectionN_btn = PhotoImage(file="images/intersectionN.png")
        self.intersectionE_btn = PhotoImage(file="images/intersectionE.png")
        self.intersectionS_btn = PhotoImage(file="images/intersectionS.png")
        self.intersectionO_btn = PhotoImage(file="images/intersectionO.png")
        self.void_btn = PhotoImage(file="images/vide.png")

        
        # CREATE A DUMMY BUTTON WITH ONE OF THE IMAGE WE LOADED ON master OF IT #
        self.droiteH_label = Label(image=self.droiteH_btn)
        self.droiteV_label = Label(image=self.droiteV_btn)
        self.virageNE_label = Label(image=self.virageNE_btn)
        self.virageNO_label = Label(image=self.virageNO_btn)
        self.virageSE_label = Label(image=self.virageSE_btn)
        self.virageSO_label = Label(image=self.virageSO_btn)
        self.intersectionN_label = Label(image=self.intersectionN_btn)
        self.intersectionE_label = Label(image=self.intersectionE_btn)
        self.intersectionS_label = Label(image=self.intersectionS_btn)
        self.intersectionO_label = Label(image=self.intersectionO_btn)
        self.void_label = Label(image=self.void_btn)

        # CREATE A REAL BUTTON THAT ACTIVATES WHEN YOU PRESS ON THE DUMMY BUTTON CORRESPONDING
        self.buttonDH = Button(master, image=self.droiteH_btn, command=self.write_droiteH, borderwidth=0)
        self.buttonDH.place(x=100,y=280)

        self.buttonDV = Button(master, image=self.droiteV_btn, command=self.write_droiteV, borderwidth=0)
        self.buttonDV.place(x=150,y=280)

        self.buttonVNE = Button(master, image=self.virageNE_btn,command=self.write_virageNE, borderwidth=0)
        self.buttonVNE.place(x=200, y=280)

        self.buttonVNO = Button(master, image=self.virageNO_btn,command=self.write_virageNO, borderwidth=0)
        self.buttonVNO.place(x=250, y=280)

        self.buttonVSE = Button(master, image=self.virageSE_btn,command=self.write_virageSE, borderwidth=0)
        self.buttonVSE.place(x=300, y=280)

        self.buttonVSO = Button(master, image=self.virageSO_btn,command=self.write_virageSO, borderwidth=0)
        self.buttonVSO.place(x=100, y=320)

        self.buttonIN = Button(master, image=self.intersectionN_btn, command=self.write_intersectionN, borderwidth=0)
        self.buttonIN.place(x=150, y=320)

        self.buttonIE = Button(master, image=self.intersectionE_btn, command=self.write_intersectionE, borderwidth=0)
        self.buttonIE.place(x=200, y=320)

        self.buttonIS = Button(master, image=self.intersectionS_btn, command=self.write_intersectionS, borderwidth=0)
        self.buttonIS.place(x=250, y=320)

        self.buttonIO = Button(master, image=self.intersectionO_btn, command=self.write_intersectionO, borderwidth=0)
        self.buttonIO.place(x=300, y=320)

        self.buttonVoid = Button(master, image=self.void_btn, command=self.write_void, borderwidth=0)
        self.buttonVoid.place(x=200, y=370)

        ## WRITE THE AFFECTATION OF EACH ROBOT
        self.format_infos_robot_label = Label(master,text="Affectation of each robot")
        self.format_infos_robot_label.place(x=10,y=420)

        # ROBOT 1
        self.robot1_label = Label(master, text="Robot 1", fg="black")
        self.robot1_label.place(x=10,y=460)
        self.robot1_text = Text(master, height=1, width=10)
        self.robot1_text.place(x=90,y=460)

        # ROBOT 2
        self.robot2_label = Label(master, text="Robot 2", fg="black")
        self.robot2_label.place(x=10,y=500)
        self.robot2_text = Text(master, height=1, width=10)
        self.robot2_text.place(x=90,y=500)

        # ROBOT 3
        self.robot3_label = Label(master, text="Robot 3", fg="black")
        self.robot3_label.place(x=10,y=540)
        self.robot3_text = Text(master, height=1, width=10)
        self.robot3_text.place(x=90,y=540)

        # ROBOT 4
        self.robot4_label = Label(master, text="Robot 4", fg="black")
        self.robot4_label.place(x=10,y=580)
        self.robot4_text = Text(master, height=1, width=10)
        self.robot4_text.place(x=90,y=580)

        # ROBOT 5
        self.robot5_label = Label(master, text="Robot 5", fg="black")
        self.robot5_label.place(x=10,y=620)
        self.robot5_text = Text(master, height=1, width=10)
        self.robot5_text.place(x=90,y=620)

        # ROBOT 6
        self.robot6_label = Label(master, text="Robot 6", fg="black")
        self.robot6_label.place(x=220,y=460)
        self.robot6_text = Text(master, height=1, width=10)
        self.robot6_text.place(x=300,y=460)

        # ROBOT 7
        self.robot7_label = Label(master, text="Robot 7", fg="black")
        self.robot7_label.place(x=220,y=500)
        self.robot7_text = Text(master, height=1, width=10)
        self.robot7_text.place(x=300,y=500)

        # ROBOT 8
        self.robot8_label = Label(master, text="Robot 8", fg="black")
        self.robot8_label.place(x=220,y=540)
        self.robot8_text = Text(master, height=1, width=10)
        self.robot8_text.place(x=300,y=540)

        # ROBOT 9
        self.robot9_label = Label(master, text="Robot 9", fg="black")
        self.robot9_label.place(x=220,y=580)
        self.robot9_text = Text(master, height=1, width=10)
        self.robot9_text.place(x=300,y=580)

        # ROBOT 10
        self.robot10_label = Label(master, text="Robot 10", fg="black")
        self.robot10_label.place(x=220,y=620)
        self.robot10_text = Text(master, height=1, width=10)
        self.robot10_text.place(x=300,y=620)

        ## WRITE THE POSITION OF SPECIAL POINTS (e.g HOSPITALS, VICTIMS)
        self.SP_label = Label(master, text="OPTIONAL EMPLACEMENTS")
        self.SP_label.place(x=10, y=660)

        # HOSPITALS
        self.hospitals_label = Label(master, text="Hospitals", fg="black")
        self.hospitals_label.place(x=10,y=700)
        self.hospitals_text = Text(master, height=1, width=10)
        self.hospitals_text.place(x=90, y=700)

        # VICTIMS
        self.victims_label = Label(master, text="Victims", fg="black")
        self.victims_label.place(x=220,y=700)
        self.victims_text = Text(master, height=1, width=10)
        self.victims_text.place(x=300,y=700)



    ####################
    #### END WINDOW ####
    ####################






    ####################
    ##### FUNCTIONS ####
    ####################

    ## DISPLAY HELP ON HOW TO WRITE A GOOD CONFIG FILE ##
    def aide(self):
        show_help = masterlevel()
        show_help.geometry("800x250")
        show_help.title("Need help?")
        message = Label(show_help,text=self.help_message(),justify="left",fg="black",font=("Arial",14))
        message.place(x=10, y=50)

    def help_message(self):
        message = "Correct format for robot affectation: id_player,x,y,orientation, e.g 2,5,3,N\n\n"
        message += "Correct format for special points positions: x1,y1;x2,y2\n\n"
        message += "You can learn more about this program by seaching the repository LeDirge/DriveToGaether"
        return message

    ## TO CREATE A NEW FILE ##
    def new(self):
        self.file_save = filedialog.asksaveasfilename(defaultextension=".txt", initialdir = ".", title="New", filetypes=(("txt Files", "*.txt"), ("All files","*.*")))
        if self.file_save:
            self.file_save = open(self.file_save,'w')
            self.file_save.close()


    ## TO SAVE TEXT ON AN ALREADY CREATED FILE ##
    def save(self):
        global file_name
        try:
            if file_name:
                nb_joueurs = self.text_players.get(1.0, END)
                nb_robots = self.text_robots.get(1.0, END)
                nb_rows = self.text_rows.get(1.0, END)
                nb_col = self.text_col.get(1.0,END)
                affectation = self.all_robots_informations()
                special_points = self.all_SP_informations()
                if self.test_format_int(nb_joueurs,nb_robots,nb_rows,nb_col) and self.test_format_SP(special_points):
                    self.file_save = open(file_name,'w')
                    self.file_save.write("## NB PLAYERS ##\n"+nb_joueurs)
                    self.file_save.write("## NB ROBOTS ##\n"+nb_robots)
                    self.file_save.write("## INFOS ROBOTS ##\n"+affectation)
                    if len(special_points) != 0:
                        self.file_save.write("## SPECIAL POINTS ##\n"+special_points)
                    dimension = str("row:"+nb_rows+"column:"+nb_col)
                    dimension = dimension.replace("\n", " ",1)
                    self.file_save.write("## DIMENSION ##\n"+dimension)
                    self.file_save.write("## GROUND ##\n"+self.text_ground.get(1.0, END))
                    self.file_save.close()
        except Exception:
            print("Something went wrong while saving, check that there's not any format problem in the file you filled")

    ## TO SAVE TEXT ON A NEW FILE ##
    def save_as(self):
        self.file_save = filedialog.asksaveasfilename(defaultextension=".txt", initialdir = ".", title="Save File As", filetypes=(("txt Files", "*.txt"), ("All files","*.*")))
        try:
            if self.file_save:
                nb_joueurs = self.text_players.get(1.0, END)
                nb_robots = self.text_robots.get(1.0, END)
                nb_rows = self.text_rows.get(1.0, END)
                nb_col = self.text_col.get(1.0,END)
                affectation = self.all_robots_informations()
                special_points = self.all_SP_informations()
                if self.test_format_int(nb_joueurs,nb_robots,nb_rows,nb_col) and self.test_format_SP(special_points):
                    self.file_save = open(self.file_save,'w')
                    self.file_save.write("## NB PLAYERS ##\n"+nb_joueurs)
                    self.file_save.write("## NB ROBOTS ##\n"+nb_robots)
                    self.file_save.write("## INFOS ROBOTS ##\n"+affectation)
                    if len(special_points) != 0:
                        self.file_save.write("## SPECIAL POINTS ##\n"+special_points)
                    dimension = str("row:"+nb_rows+"column:"+nb_col)
                    dimension = dimension.replace("\n", " ",1)
                    self.file_save.write("## DIMENSION ##\n"+dimension)
                    self.file_save.write("## GROUND ##\n"+self.text_ground.get(1.0, END))
                    self.file_save.close()
        except Exception:
            print("Something went wrong while saving, check that there's not any format problem in the file you filled")

    ## TO OPEN A FILE ##
    def open_file_function(self):
        self.file_save = filedialog.askopenfilename(initialdir = ".", title = "Select file", filetypes = (("txt files", "*.txt"), ("All files", "*.*")))
        self.master.title(f'{self.file_save}')
        self.text_players.delete(1.0,END)
        self.text_robots.delete(1.0,END)
        self.text_col.delete(1.0,END)
        self.text_rows.delete(1.0,END)
        self.text_ground.delete(1.0,END)
        self.robot1_text.delete(1.0,END)
        self.robot2_text.delete(1.0,END)
        self.robot3_text.delete(1.0,END)
        self.robot4_text.delete(1.0,END)
        self.robot5_text.delete(1.0,END)
        self.robot6_text.delete(1.0,END)
        self.robot7_text.delete(1.0,END)
        self.robot8_text.delete(1.0,END)
        self.robot9_text.delete(1.0,END)
        self.robot10_text.delete(1.0,END)
        self.hospitals_text.delete(1.0,END)
        self.victims_text.delete(1.0,END)
        if self.file_save:
            global file_name
            file_name = self.file_save
        try:
            with open(self.file_save) as file:
                for line in file:
                    #print(line)
                 
                    if "NB PLAYERS" in line: #if the line contains "PLAYERS", the next line should hold the number of players
                            players = str(file.readline())
                            players = players.replace("\n","")
                            self.text_players.insert(INSERT,players)
                            
                    if "NB ROBOTS" in line: #if the line contains "ROBOTS", the next line should hold the number of probots
                        robots = str(file.readline())
                        robots = robots.replace("\n","")
                        self.text_robots.insert(INSERT,str(robots))
                        
                    if "DIMENSION" in line: #if the line contains "DIMENSION", the next line should hold the dimension of the terrain
                        ligne = str(file.readline())
                        ligne = ligne.split(" ")
                        for dim in ligne:
                            if "row" in dim:
                                row = dim.split(":")[1]
                                row = row.replace("\n","")
                                self.text_rows.insert(INSERT,str(row))
                            elif "col" in dim:
                                col = dim.split(":")[1]
                                col = col.replace("\n","")
                                self.text_col.insert(INSERT,str(col))
                            
                    if "INFOS ROBOTS" in line: #if the line contains "IDENTIF", the next line should hold informations about the robots
                        line = str(file.readline())
                        line = line.replace("\n","")
                        line = line.split(" ")
                        for infos in line:
                            infos = infos.split(":")

                            if infos[0] == "1":
                                self.robot1_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "2":
                                self.robot2_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "3":
                                self.robot3_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "4":
                                self.robot4_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "5":
                                self.robot5_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "6":
                                self.robot6_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "7":
                                self.robot7_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "8":
                                self.robot8_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "9":
                                self.robot9_text.insert(INSERT,str(infos[1]))

                            if infos[0] == "10":
                                self.robot10_text.insert(INSERT,str(infos[1]))

                    if "SPECIAL POINTS" in line:
                        infos = str(file.readline())
                        infos = infos.replace("\n","")
                        infos = infos.split(" ")

                        if len(infos) > 2:
                            raise Exception

                        coord_l_v = [] # list of the coordinates of the victims
                        coord_l_h = [] # list of the coordinates of the hospitals

                        for coord in infos:
                            if "H" in coord:
                                h = infos[0].split(":")[1].split(";") # hold the coordinates of the hospitals
                                for coord_h in h:
                                    coord_h = coord_h.split(",")
                                    coord_l_h.append([coord_h[0],coord_h[1]])

                            if "V" in coord:
                                v = infos[1].split(":")[1].split(";") # hold the coordinates of the victims
                                for coord_v in v:
                                    coord_v = coord_v.split(",")
                                    coord_l_v.append([coord_v[0],coord_v[1]])

                        if len(coord_l_v) !=0 :
                            text_coord="" # will hold the text version of the coordinates from the victims
                            for coord in coord_l_v: # coord_l_v is a list of lists, we need to "join" each sub-list
                                text_coord+=",".join(coord)+";"
                            text_coord = "".join(text_coord.rsplit(";",1))
                            self.victims_text.insert(INSERT,text_coord)

                        if len(coord_l_h) !=0 :
                            text_coord="" # will hold the text version of the coordinates from the hospitals
                            for coord in coord_l_h: # coord_l_h is a list of lists, we need to "join" each sub-list
                                text_coord+=",".join(coord)+";"
                            text_coord = "".join(text_coord.rsplit(";",1))
                            self.hospitals_text.insert(INSERT,text_coord)

                    if "GROUND" in line:
                        line = file.readlines()
                        line = "".join(line)
                        self.text_ground.insert(INSERT,line)

        except Exception:
            showinfo(title="Warning!", message="You either did not choose a file to open or the file contains errors!")


    ## INSURE THAT EVERY INTEGER INPUT REALLY RECEIVED A INTEGER ##
    def test_format_int(self, nb_joueurs, nb_robots, nb_rows, nb_col):
        try:
            return isinstance(int(nb_joueurs),int) and isinstance(int(nb_robots), int) and isinstance(int(nb_rows),int) and isinstance(int(nb_col),int)
        except Exception:
            showerror(title="Format error",message="Beware, you tried to put a character in an input that requires an integer!")

    ## INSURE THAT THE COORDINATES OF THE  SPECIAL POINTS ARE CORRECTLY WRITTEN
    def test_format_SP(self,special_points):
        if len(special_points) != 0: # if the user entered some special points, we test them
            infos = special_points.split(" ")
            infos_h = [coord for coord in infos if "H" in coord]
            infos_v = [coord for coord in infos if "V" in coord]

            coord_h = infos_h[0].split(":")[1].split(";") # it first creates 2 new lists: one with "H" and the other with the coordinates all stuck together. 
            # We then split the second one on a new list we each entry = a pair of x and y
            test_h = [] # each entry of this list will be either a x or a y from coord_h
            for parcours in coord_h:
                x = int(parcours.split(",")[0])
                y = int(parcours.split(",")[1])
                test_h.append(x)
                test_h.append(y)

            if len(test_h)%2:
                raise Exception("There's an error in the coordinates of the hospitals")

            coord_v = infos_v[0].split(":")[1].split(";") # it first creates 2 new lists: one with "V" and the other with the coordinates all stuck together. 
            # We then split the second one on a new list we each entry = a pair of x and y
            test_v = [] # each entry of this list will be either a x or a y from coord_v
            for parcours in coord_v:
                x = int(parcours.split(",")[0])
                y = int(parcours.split(",")[1])
                test_v.append(x)
                test_v.append(y)

            if len(test_v)%2: # in case there's a x or a y missing
                raise Exception("There's an error in the coordinates of the victims")

        return True

    ## RETRIEVE ALL THE INFORMATIONS FROM THE ROBOTS ##
    def all_robots_informations(self):
        infos = ""
        nb = 0 # count the number of informations that we added to "infos"
        if len(self.robot1_text.get(1.0,END)) != 1:
            infos+="1:"+self.robot1_text.get(1.0,END)
            nb += 1

        if len(self.robot2_text.get(1.0,END)) != 1:
            infos+="2:"+self.robot2_text.get(1.0,END)
            nb += 1

        if len(self.robot3_text.get(1.0,END)) != 1:
            infos+="3:"+self.robot3_text.get(1.0,END)
            nb += 1

        if len(self.robot4_text.get(1.0,END)) != 1:
            infos+="4:"+self.robot4_text.get(1.0,END)
            nb += 1

        if len(self.robot5_text.get(1.0,END)) != 1:
            infos+="5:"+self.robot5_text.get(1.0,END)
            nb += 1

        if len(self.robot6_text.get(1.0,END)) != 1:
            infos+="6:"+self.robot6_text.get(1.0,END)
            nb += 1

        if len(self.robot7_text.get(1.0,END)) != 1:
            infos+="7:"+self.robot7_text.get(1.0,END)
            nb += 1

        if len(self.robot8_text.get(1.0,END)) != 1:
            infos+="8:"+self.robot8_text.get(1.0,END)
            nb += 1

        if len(self.robot9_text.get(1.0,END)) != 1:
            infos+="9:"+self.robot9_text.get(1.0,END)
            nb += 1

        if len(self.robot10_text.get(1.0,END)) != 1:
            infos+="10:"+self.robot10_text.get(1.0,END)
            nb += 1

        infos = infos.replace("\n"," ",nb-1)
        return infos

    ## RETRIEVE THE INFORMATIONS OF SPECIAL POINTS (SP)
    def all_SP_informations(self):
        infos = ""
        nb = 0 # count the number of informations that we added to "infos"
        if len(self.hospitals_text.get(1.0,END)) != 1:
            infos+="H:"+self.hospitals_text.get(1.0,END)
            nb+=1
        if len(self.victims_text.get(1.0,END)) != 1:
            infos+="V:"+self.victims_text.get(1.0,END)
            nb+=1
        infos = infos.replace("\n"," ",nb)
        infos = "".join(infos.rsplit(" ",1)) ## replace only the last whitespace, which caused an error in the config file
        infos += "\n"
        return str(infos)



    ## WRITE A NUMBER ON THE GROUND REPRESENTATION THAT DEPENDS ON WHAT BUTTON YOU PRESSED ##
    def write_void(self):
        self.text_ground.insert(END,"0 ")
    
    def write_droiteH(self): # IF STRAIGHT HORIZONTAL LINE
        self.text_ground.insert(END,"1 ")

    def write_droiteV(self): # IF STRAIGHT VERTICAL LINE
        self.text_ground.insert(END,"2 ")

    def write_virageNE(self): # IF RIGHT TURN FROM NORTH
        self.text_ground.insert(END,"3 ")

    def write_virageNO(self): # IF LEFT TURN FROM NORTH
        self.text_ground.insert(END,"4 ")

    def write_virageSE(self): # IF RIGHT TURN FROM SOUTH
        self.text_ground.insert(END,"5 ")

    def write_virageSO(self): # IF LEFT TURN FROM SOUTH
        self.text_ground.insert(END,"6 ")

    def write_intersectionN(self): # IF INTERSECTION FACING NORTH
        self.text_ground.insert(END,"7 ")

    def write_intersectionE(self): # IF INTERSECTION FACING EAST
        self.text_ground.insert(END,"8 ")

    def write_intersectionS(self): # IF INTERSECTION FACING SOUTH
        self.text_ground.insert(END,"9 ")

    def write_intersectionO(self): # IF INTERSECTION FACING WEST
        self.text_ground.insert(END,"10 ")

    ####################
    ## END FUNCTIONS ###
    ####################