# CONFIG 
!!! PREMIERE VERISION, PEUT ETRE AMENEE A CHANGER VOIRE ENTIEREMENT DISPARAITRE !!!

How to create the config file:
  You need to have five (5) categories: NB PLAYERS, NB ROBOTS, IDENTIF PLAYER, DIMENSION, GROUND. 
  The name of each category needs to appear a row before their value.  
  For NB PLAYERS, NB ROBOTS, IDENTIF PLAYER, DIMENSION their order in the config file doesn't matter.  
  The GROUND category **NEEDS** to be the last one.
  
  ## FORMAT
  ### NB PLAYERS :
  After writing the name of this category, the next row will have its value.
  
  ### NB ROBOTS :
  Same as NB PLAYERS.
  
  ### IDENTIF PLAYERS :
  After writing the name of this category, the next row needs to follow a certain format, that is:
  id_player:robot_number or, in case the player has several robots to command, id_player:robot_number_1,robot_number_2,... ; e.g 2:1,4,6, which means that the player number 2 controls the robot number 1, 4 and 6.
  
  ### DIMENSION :
  After writing the name of this category, the next row need to follow a certain format, that is:
  row:number_of_rows column:number_of_columns ; e.g row:3 column:7 .
  You can also intervert the order; e.g column:7 row:3 .

  ### GROUND :
  After writing the name of this category, the next row needs to follow a certain format.
  The terrain should resemble a rectangle matrix. Each value represents a type of tile; e.g a straight horizontal line could be a one (1).
  An empty tile is represented by a zero (0).
  
  ### EXAMPLE OF VALID FILE
  ### NB PLAYERS 
  3
  ### NB ROBOTS 
  5
  ### IDENTIF PLAYER 
  1:1,5,2 2:3 3:4
  ### DIMENSION 
  row:3 column:7
  ### GROUND 
  1 2 3 11 10 11 10
  4 5 6 0 0 0 0
  7 8 9 0 0 0 0
  
  ## USAGE
  ```sh
  ./python3 traitementConfig.py <config_file.txt> <number_of_possible_tiles>
  ```
  ### EXAMPLE
 ```sh
 ./python3 traitementConfig.py example_config.txt 12
