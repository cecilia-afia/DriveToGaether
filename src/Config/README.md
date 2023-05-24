# CONFIG 
!!! VERSION DEFINITIVE, PEUT ETRE AMENEE A LEGEREMENT CHANGER !!!

How to create the config file **MANUALLY**:
  You need to have five (5) categories: NB PLAYERS, NB ROBOTS, INFOS ROBOTS, SPECIAL POINTS, DIMENSION, GROUND. 
  The name of each category needs to appear a row before their value.
  The SPECIAL POINTS section is optional, don't write it if there's nothing to write.
  For NB PLAYERS, NB ROBOTS, INFOS ROBOTS, DIMENSION and SPECIAL POINTS, their order in the config file doesn't matter.  
  The GROUND category **NEEDS** to be the last one.
  You can't have unecessary whitespaces (especially at the end of a line), you can't have empty line(s) between two (2) categories.
  
  ## FORMAT
  ### NB PLAYERS :
  After writing the name of this category, the next row will have its value.
  
  ### NB ROBOTS :
  Same as NB PLAYERS.
  
  ### INFOS ROBOTS :
  After writing the name of this category, the next row needs to follow a precise format, that is:
  robot_number: x_starting_point,y_starting_point,orientation e.g 2:1,4,N, which means that the robot number 2 starts at the coordinates [1,4] facing North.

  ### SPECIAL POINTS :
  This section is optional.
  After writing the name of this category, the next row need to follow a precise format, that is:
  H:x_first_hospital,y_first_hospital V:x_first_victim,y_first_victim; e.g H:2,5 V:3,6

  If there is several hospitals/victims, you need to separate them with a ";", e.g H:x_first_hospital,y_first_hospital;x_second_hospital,y_second_hospital V:x_first_victim,y_first_victim; e.g H:2,5;3,7 V:3,6
  You can have only hospitals or only victims in the file.
  You can also intervert the order; e.g V:3,6 H:2,5;3,7
  
  ### DIMENSION :
  After writing the name of this category, the next row need to follow a precise format, that is:
  row:number_of_rows column:number_of_columns ; e.g row:3 column:7 .
  You can also intervert the order; e.g column:7 row:3 .

  ### GROUND :
  After writing the name of this category, the next row needs to follow a certain format.
  The terrain should resemble a rectangle matrix. Each value represents a type of tile; e.g a straight horizontal line could be a one (1).
  An empty tile is represented by a zero (0).
  
  ### EXAMPLE OF VALID FILE:

  ### NB PLAYERS 
  2
  ### NB ROBOTS 
  2
  ### INFOS ROBOTS 
  2:5,1,S 3:9,8,E
  ### DIMENSION 
  row:3 column:7
  ### GROUND 
  1 2 3 11 10 11 10
  4 5 6 0 0 0 0
  7 8 9 0 0 0 0
  
  ## USAGE
  ```sh
  $python3 traitementConfig.py <config_file.txt> <number_of_possible_tiles>
  ```
  ### EXAMPLE
 ```sh
  $python3 traitementConfig.py example_config.txt 12
 ```

How to create the config file with the GUI:

## USAGE
```sh
  $python3 editeurConfig.py
  ```
## EDIT A FILE
If you want to edit an already created config file, click on "File">"Open".
All the informations in it should appear on the GUI, unless the format of the file is incorrect (especially if you created it manually).
Once modified, click on "File">"Save".

## CREATE A FILE
If you want to create a new one, click on "File">"New" OR fill all the blanks (the section "OPTIONAL EMPLACEMENTS", is, as the name suggests, optional) and click on "File">"Save As".
If you clicked on "New", write the name of the file and then open it (c.f "EDIT A FILE" section) to fill it.

## ERRORS
Most of the errors will be written in the terminal you used to open the GUI, keep an eye on it!