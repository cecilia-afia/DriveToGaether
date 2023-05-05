# SERVEUR

!!! POUR LE MOMENT, CETTE METHODE NE SERT QUE POUR LES TESTS (ENVOI DE MESSAGE AU TOUR PAR TOUR SUR DES MACHINES DISTANTES) ET PEUT ETRE AMENEE A CHANGER VOIRE ENTIEREMENT DISPARAITRE !!!

In both cases:
-
- Install Hamachi : https://www.vpn.net/linux
  - Install Haguichi (allow to use Hamachi on Linux):  
  ```sh 
  sudo add-apt-repository -y ppa:ztefn/haguichi-stable
  sudo apt update
  sudo apt install -y haguichi
  ```
  - Run Haguichi :
  ```sh
  haguichi&
  ```
  - Configure haguichi by pressing "Configure" (doesn't need any humain input)
<<<<<<< HEAD:src/Serveur/README.md
  - Retrieve ipv4 of the server from Haguichi or Hamachi
=======
  
To run the server:
  -
  - Create a new network with Haguichi (Linux) or Hamachi (Windows)
  - Retrieve ipv4 adress from Haguichi/Hamachi and pass it to the "host" variable in "serverSocket.py"
>>>>>>> 20147c1 (Update REAMDE.md):src/Serveur/REAMDE.md
  - Run "serverPocket.py":
  ```sh
  python3 serverSocket.py <server_ipv4>
  ```
  - Choose a port number (all the clients need the same)
  - Wait for the clients to connect

To run the client:
   -
<<<<<<< HEAD:src/Serveur/README.md
   - Connect to the server with Hamachi
   - Wait for the server to be ready
   - Retrieve the hostname (should be printed when the server is being runned)
   - Run "clientSocket.py":
   ```sh
  python3 clientSocket.py <server_ipv4>
  ```
   - Retrieve the port number (should be printed when the server is being runned) and enter it
=======
   - Join the netwotk of the server with Haguichi (Linux) or Hamachi (Windows)
   - Wait for the server to be running
   - Retrieve the hostname (should be printed when the server is being runned) and pass it to the "host" variable in "clientSocket.py"
   - Retrieve the port number (should be printed when the server is being runned) and pass it to the "port" variable in "clientSocket.py"
>>>>>>> 20147c1 (Update REAMDE.md):src/Serveur/REAMDE.md
   - Send the cutest message to the server you've got
   - Hope it works
