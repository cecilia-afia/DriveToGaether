import numpy as np
import sys


## TEST NUMBER OF ARGUMENTS ##

if len(sys.argv) != 3:
	print("Usage : %s <config_file.txt> <number_of_tiles_possible>"%sys.argv[0])
	exit(1)

## END TEST NUMBER OF ARGUMENTS ##

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

## END TEST NUMBER OF LINES ##

## FUNCTIONS ##

## this function is used to convert a str to an int in the function np.loadtxt()
## if the value that is converted to an int is greater than nbPossibleTiles, an exception is raised

def conv(val):
	if (int(val) < nbPossibleTiles):
		return int(val)
	raise Exception(ValueError)

## this function is used to count the number of values in a dictionnary.
## in our case, it helps determine if there's the same number of robots in the catergory "NB ROBOTS" and in the dictionnary depicting the repartion of the robots

def countDict(dict):
	count = 0
	for c in dict:
		if isinstance(dict[c],list):
			count += len(dict[c])
		else:
			count += 1
	return count


## END FUNCTIONS ##

try:
	nb_categories = 0
	with open(sys.argv[1]) as file:

		for line in file:
			#print(line)
			try: 
				if "PLAYERS" in line: #if the line contains "PLAYERS", the next line should hold the number of players
						players = int(file.readline())
						print("\nnb players = ",players)
						nb_categories += 1
			except Exception:
				print("There's a problem with the number of players")
				exit(4)

			try:
				if "ROBOTS" in line: #if the line contains "ROBOTS", the next line should hold the number of probots
					robots= int(file.readline())
					print("\nnb robots = ",robots)
					nb_categories += 1

			except Exception:
				print("There's a problem with the number of robots")
				exit(4)

			try:
				if "DIMENSION" in line: #if the line contains "DIMENSION", the next line should hold the dimension of the terrain
					ligne = str(file.readline())
					ligne = ligne.split(" ")
					print(ligne)
					for dim in ligne:
						if "row" in dim:
							row = int(dim.split(":")[1])
						elif "col" in dim:
							col = int(dim.split(":")[1])
						else:
							raise Exception("Error while reading the dimension of the terrain")
					print("Nb rows: ",row,"\nNb columns: ",col)
			except Exception as error:
				print(error)
				exit(5)

			try:


				if "IDENTIF" in line: #if the line contains "IDENTIF", the next line should hold the repartition of the robots
					dic_identif = {}
					ligne = str(file.readline())
					ligne = ligne.replace(','," ")
					ligne = ligne.split(" ")
					for mot in ligne:
						if ":" in mot: # if this is a new player, the format of "mot" will be player_id:robot_id, exemple: 2:5

							mot = mot.split(":")
							cle = mot[0]

							if cle in dic_identif:
								dic_identif[cle].append(int(mot[1]))
							else:
								dic_identif[cle] = [int(mot[1])]

						else:
							dic_identif[cle].append(int(mot))

					## TEST NUMBER PLAYERS ##
					if len(dic_identif) != players:
						raise Exception("There's not the same number of players in the dictionnary of affectation that the number of players in the config file")
					## END TEST NUMBER PLAYERS ##

					## TEST NUMBER ROBOTS ##
					if countDict(dic_identif) != robots:
						raise Exception("There's not the same number of robots in the dictionnary of affectation that the number of robots in the config file")
					## END TEST NUMBER ROBOTS ##

					print("\nRépartition des robots :\n",dic_identif)
					nb_categories += 1

			except Exception as error:
				print(error)
				exit(5)


			if line == "\n":
				raise Exception("You can't have an empty line in your config.txt")
		

		if nb_categories != 3:
			raise Exception("There's not enough informations in the config.txt; you need to have at least the three following: ## NB PLAYERS ##, ## NB ROBOTS ##, ## IDENTIF PLAYER ##")


except Exception as error:
	print(error)
	exit(3)


try:
	matrix = np.loadtxt(sys.argv[1],skiprows=9,converters=conv) # if no mistakes were made before, the matrix representing the terrain will start at row 10

except ValueError:
	print("\nThere's an error in the terrain representation; \ncheck that every row has the same length; \ncheck that every value is a number; \ncheck that every number is lesser than",sys.argv[2],"which is the number of tiles possible; \nthe terrain representation NEEDS to be the last thing of the config file")
	exit(4)

try:
	if (row != matrix.shape[0] or col != matrix.shape[1]):
		raise Exception("The dimension of the terrain is not the same in the representation and in the values you entered in the category DIMENSION")

except Exception as error:
	print(error)
	exit(6)

print("\nVue d'ensemble du terrain : \n",matrix,"\n")