import numpy as np
import sys


## TEST NUMBER OF ARGUMENTS ##

if len(sys.argv) != 3:
	print("Usage : %s <config_file.txt> <number_of_tiles_possible>"%sys.argv[0])
	exit(1)

## END TEST NUMBER OF ARGUMENTS ##

nbPossibleTiles = int(sys.argv[2]) #stores the number of possible tiles 

## this function is used to convert a str to an int in the function np.loadtxt()
## if the value that is converted to an int is greater than nbPossibleTiles, an exception is raised
def conv(val):
	if (int(val) < nbPossibleTiles):
		return int(val)
	raise Exception(ValueError)

## test if a line is empty
def isNotNull(line):
	if line == "":
		return False
	return True	

## TEST NUMBER OF LINES ##
## if the number of line is lesser than 8, it means there's not enough lines to have a fully
## usable config.txt
try: 
	with open("config.txt") as file:
			nb_lignes = len(file.readlines())
			if nb_lignes < 8:
				raise Exception("There's not enough lines in your config.txt")
except Exception as error:
	print(error)
	exit(2)

## END TEST NUMBER OF LINES ##


try:
	nb_categories = 0
	with open("config.txt") as file:

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

					print("\nRépartition des robots :\n",dic_identif)
					nb_categories += 1

			except Exception:
				print("There's a problem with the repartion of the robots")
				exit(4)


			if line == "\n":
				raise Exception("You can't have an empty line in your config.txt")
		

		if nb_categories != 3:
			raise Exception("There's not enough informations in the config.txt; you need to have at least the three following: ## NB PLAYERS ##, ## NB ROBOTS ##, ## IDENTIF PLAYER ##")


except Exception as error:
	print(error)
	exit(3)


try:
	matrix = np.loadtxt(sys.argv[1],skiprows=7,converters=conv) # if no mistakes were made before, the matrix representing the terrain will start at row 8
except ValueError:
	print("\nThere's an error in the terrain representation; \ncheck that every row has the same length; \ncheck that every value is a number; \ncheck that every number is lesser than",sys.argv[2],"which is the number of tiles possible; \nthe terrain representation NEEDS to be the last thing of the config file")
	exit(4)


print("\nVue d'ensemble du terrain : \n",matrix,"\n")