import numpy as np
import sys
from tile import Tile

	####################
    ##### FUNCTIONS ####
    ####################

## this function is used to convert a str to an int in the function np.loadtxt()
## if the value that is converted to an int is greater than nbPossibleTiles, an exception is raised

def conv(val):
	if (int(val) <= nbPossibleTiles):
		return int(val)
	raise Exception(ValueError)

## this function is used to count the number of values in a dictionnary.
## in our case, it helps determine if there's the same number of robots in the catergory "NB ROBOTS" and in the dictionnary depicting the repartion of the robots

"""
def countDict(dict): ## UNUSED 
	count = 0
	for c in dict:
		if isinstance(dict[c],list):
			count += len(dict[c])
		else:
			count += 1
	return count 
"""

## this function checks if the input "value" is truly an orientation
def is_orientation(value):
	return value == "N" or value == "S" or value == "E" or value == "W"

## return a Tile object accordingly to the value extracted from the config file
def create_tile(value):
	if value == 1:
		return Tile(0,1,0,1)
	if value == 2:
		return Tile(1,0,1,0)
	if value == 3:
		return Tile(1,1,0,0)
	if value == 4:
		return Tile(1,0,0,1)
	if value == 5:
		return Tile(0,1,1,0)
	if value == 6:
		return Tile(0,0,1,1)
	if value == 7:
		return Tile(1,1,0,1)
	if value == 8:
		return Tile(1,1,1,0)
	if value == 9:
		return Tile(0,1,1,1)
	if value == 10:
		return Tile(1,0,1,1)
	else:
		return Tile(2,2,2,2) # if the value is 0, it only means there's no tile here, but it's still in the perimeter of the terrain

# test if the actual tile is compatible with his left neigbhor
def is_compatible_left(actual_tile, left_tile): 
    return (actual_tile.W == left_tile.E) or (actual_tile.W == 2) or (left_tile.E == 2)

# test if the actual tile is compatible with his up neigbhor
def is_compatible_up(actual_tile, up_tile): 
    return (actual_tile.N == up_tile.S) or (actual_tile.W == 2) or (up_tile.E == 2)

# test if the positions are in the grid
def positions_are_valide(tuple_pos, row, col):
	return tuple_pos[0]*tuple_pos[1] <= (row-1) * (col-1) #we need to decrement row and col, tuple_pos could be (0,0) wich is the upper-left tile

	####################
    ## END FUNCTIONS ###
    ####################



	####################
    ###### MAIN ########
    ####################
if __name__ == '__main__':
	####################
    ####### TESTS ######
    ####################

	## TEST CORRECT USAGE
	if len(sys.argv) != 3:
		print("Usage : %s <config_file.txt> <number_of_tiles_possible>"%sys.argv[0])
		exit(1)

	## END TEST CORRECT USAGE ##

	nbPossibleTiles = int(sys.argv[2]) #stores the number of possible tiles 

	## TEST NUMBER OF LINES ##
	## if the number of line is lesser than 8, it means there's not enough lines to have a fully
	## usable config.txt
	try: 
		with open(sys.argv[1]) as file:
				nb_lignes = len(file.readlines())
				if nb_lignes < 8:
					raise Exception("There's not enough lines in your config.txt")
	except Exception as error:
		print(error)
		exit(2)

		####################
	    ##### END TESTS ####
	    ####################


	####################
    ##### VARIABLES ####
    ####################

	tile_is_valid = True # is used when we determine if a tile is compatible with its neighbors
	nb_lignes = 0 # will help determine how many lines the "np.loadtxt()" function will need to skip to get to the terrain representation
	coord_l_v = [] # list of the coordinates of the victims, will stay empty if there's no victim
	coord_l_h = [] # list of the coordinates of the hospitals

	####################
    ### END VARIABLES ##
    ####################

	try:
		nb_categories = 0
		with open(sys.argv[1]) as file:

			for line in file:
				#print(line)
				
				try: 
					if "NB PLAYERS" in line: #if the line contains "NB PLAYERS", the next line should hold the number of players
							players = int(file.readline())
							print("\nnb players = ",players)
							nb_categories += 1
							nb_lignes += 2
				except Exception:
					print("There's a problem with the number of players")
					exit(4)

				try:
					if "NB ROBOTS" in line: #if the line contains "NB ROBOTS", the next line should hold the number of probots
						robots= int(file.readline())
						print("\nnb robots = ",robots)
						nb_categories += 1
						nb_lignes += 2

				except Exception:
					print("There's a problem with the number of robots")
					exit(4)

				try:
					if "DIMENSION" in line: #if the line contains "DIMENSION", the next line should hold the dimension of the terrain
						ligne = str(file.readline())
						ligne = ligne.split(" ")
						for dim in ligne:
							if "row" in dim:
								row = int(dim.split(":")[1])
							elif "col" in dim:
								col = int(dim.split(":")[1])
							else:
								raise Exception("Error while reading the dimension of the terrain")
						print("Nb rows: ",row,"\nNb columns: ",col)
						nb_categories += 1
						nb_lignes += 2

				except Exception as error:
					print(error)
					exit(5)

				try: 
					if "INFOS ROBOTS" in line: #if the line contains "INFOS ROBOTS", the next line should hold the repartition of the robots
						dic_identif = {}
						ligne = str(file.readline())
						ligne = ligne.split(" ")
						for robot_info in ligne:
						    robot_info = robot_info.split(":")
						    num_robot = robot_info[0]
						    robot_info = robot_info[1].split(",")
						    if len(robot_info) != 3:
						        raise Exception("Not enough informations is given for one of the robots")
						    else:
						        dic_identif[num_robot] = [] # we create a new entry in the dictionnary
						        x = 0 # will hold the x position of the starting point
						        y = 0 # will hold the y position of the starting point
						        num_info = 0
						        for infos in robot_info:
						            if num_info == 0:
						                x = int(infos) 
						            elif num_info == 1:
						                y = int(infos)
						                dic_identif[num_robot].append((x,y))
						            elif num_info == 2 and is_orientation(infos.replace("\n","")):

						                dic_identif[num_robot].append(infos.replace("\n",""))
						            else: # in case there's more than 3 informations for the robot 
						            	raise Exception("Too much informations were given for the robot number :",num_robot,"or you gave it a wrong value for the orientation")
						            num_info += 1

						        if num_info != 3: # if all 3 informations are present, "num_info" will store "3". If not, the informations are incorrect
						        	raise Exception("Not enough informations were given for the robot",num_robot)

						print("\nRobots informations:\n",dic_identif)
						print("\n")
						nb_categories += 1
						nb_lignes += 2

				except Exception as error:
					print(error)
					exit(5)

				try:
					if "SPECIAL POINTS" in line:
						infos = str(file.readline()) # infos should hold a line that resembles: "H:2,5;3,2 V:3,1;3,6"
						infos = infos.split(" ")

						if len(infos) > 2:
							raise Exception

						for coord in infos:
							if "H" in coord:
								h = infos[0].split(":")[1].split(";") # hold the coordinates of the hospitals
								for coord_h in h:
									coord_h = coord_h.split(",")
									coord_l_h.append((int(coord_h[0]),int(coord_h[1])))

							elif "V" in coord:
								v = infos[1].split(":")[1].split(";") # hold the coordinates of the victims
								for coord_v in v:
								    coord_v = coord_v.split(",")
								    coord_l_v.append((int(coord_v[0]),int(coord_v[1])))
							else:
								raise Exception

						if len(coord_l_h) != 0 :
							print("Hospitals coordinates : ", coord_l_h)
						if len(coord_l_v) != 0 :
							print("Victims  coordinates : ", coord_l_v,"\n")

						nb_lignes += 2

				except Exception:
					print("There's a problem with the format of the coordinates of either the victimes, either the hospitals. Or, you added more than those two informations")
					exit(7)

				if line == "\n" and nb_categories < 4:
					raise Exception("You can't have an empty line in your config.txt")
			

			if nb_categories != 4:
				raise Exception("There's not enough informations in the config.txt; you need to have at least the four following: ## NB PLAYERS ##, ## NB ROBOTS ##, ## DIMENSION ##, ## INFOS ROBOTS ##")


	except Exception as error:
		print(error)
		exit(3)


	try:
		matrix = np.loadtxt(sys.argv[1],skiprows=nb_lignes+1,converters=conv) # if no mistakes were made before, the matrix representing the terrain will start at row 10

	except ValueError:
		print("\nThere's an error in the terrain representation; \ncheck that every row has the same length; \ncheck that every value is a number; \ncheck that every number is lesser than",sys.argv[2],"which is the number of tiles possible; \nthe terrain representation NEEDS to be the last thing of the config file")
		exit(4)

	## TEST DIMENSION VALID ##
	if (row != matrix.shape[0] or col != matrix.shape[1]):
		print(matrix.shape)
		print("The dimension of the terrain is not the same in the representation and in the value you entered in the category DIMENSION")
		exit(6)
	## END TEST DIMENSION VALID ##

	## TEST NUMBER ROBOTS ##
	if len(dic_identif) != robots:
		print("There's not the same number of robots in the dictionnary of affectation that the number of robots in the config file")
		exit(8)
	## END TEST NUMBER PLAYERS ##

	## TEST NUMBER ROBOTS ##
	"""
	if countDict(dic_identif) != robots:
		raise Exception("There's not the same number of robots in the dictionnary of affectation that the number of robots in the config file") ## UNUSED
	"""
	## END TEST NUMBER ROBOTS ##

	## TEST VALID POSITIONS OF SPECIAL POINTS ##
	try:
		if len(coord_l_v):
			for positions in coord_l_v:
				if not(positions_are_valide(positions,row,col)) and matrix[positions[0],positions[1]] != 0:
					raise Exception("The victim located at ",positions," is not in the grid or is on an empty tile")

		if len(coord_l_h):
			for positions in coord_l_h:
				print(positions)
				if not(positions_are_valide(positions,row,col)) and matrix[positions[0],positions[1]] != 0:
					raise Exception("The hospital located at ", positions, " is not in the grid or is on an empty tile")


	except Exception as error:
		print(error)
		exit(9)

	## END TEST VALID POSITIONS OF SPECIAL POINTS ##

	print("\nEncoded view of the terrain : \n",matrix,"\n")

	transformation_to_tile = np.vectorize(create_tile)
	final_matrix = transformation_to_tile(matrix)

	index = np.argwhere(matrix>0) 

	for i in index:
	    x = i[0]
	    y = i[1]
	    if x:
	        tile_is_valid = tile_is_valid and is_compatible_left(final_matrix[x,y],final_matrix[x,y-1])
	        if y:
	        	tile_is_valid = tile_is_valid and is_compatible_up(final_matrix[x,y],final_matrix[x-1,y])
	    if not(tile_is_valid):
	    	print("The tiles at the coordinates ",x,y," and ",x,y-1," or ",x-1,y," are not compatible, check them")
	    	exit(9)